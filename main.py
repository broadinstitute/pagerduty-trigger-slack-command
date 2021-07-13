import os

import flask
import pdpyras
from google.cloud import secretmanager
from google.cloud.secretmanager_v1 import AccessSecretVersionRequest
from slack.signature import SignatureVerifier

# This is the affected system which PagerDuty is reporting to be down
# See https://pagerduty.github.io/pdpyras/#events-api-client
PAGERDUTY_SOURCE = 'app.terra.bio'

secret_manager_client = secretmanager.SecretManagerServiceClient()


def secret_from_manager(secret_id: str) -> str:
    response = secret_manager_client.access_secret_version(name=secret_id)
    return response.payload.data.decode('UTF-8')


def verify_signature(request: flask.Request) -> bool:
    request.get_data()  # Decodes received requests into request.data
    verifier = SignatureVerifier(secret_from_manager(os.environ['SLACK_SIGNING_SECRET_ID']))
    return verifier.is_valid_request(request.data, request.headers)


def trigger_pagerduty(message, source):
    session = pdpyras.EventsAPISession(secret_from_manager(os.environ['PAGERDUTY_INTEGRATION_SECRET_ID']))
    session.trigger(message, source)
    return "Page initiated."


def terra_is_down(request: flask.Request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """

    if request.method != 'POST':
        return 'Only POST requests are accepted', 405

    if not verify_signature(request):
        return 'Could not verify request', 401

    # Like /terraisdown <argument>
    command_argument = request.form['text']
    page = trigger_pagerduty(command_argument, PAGERDUTY_SOURCE)
    return flask.escape(page)
