import os

import flask
from slack.signature import SignatureVerifier

# SLACK_SIGNING_SECRET: secret/suitable/terraform/pagerduty-trigger-slack-command/slack-token @ slack-signing-secret
# We might not need the client secret?
# SLACK_CLIENT_SECRET: secret/suitable/terraform/pagerduty-trigger-slack-command/slack-token @ slack-client-secret
# PAGERDUTY_INTEGRATION_SECRET: secret/suitable/pagerduty/manually-triggered-terra-incident @ events-v2-integration-key


def verify_signature(request: flask.Request) -> None:
    request.get_data()  # Decodes received requests into request.data
    verifier = SignatureVerifier(os.environ['SLACK_SIGNING_SECRET'])
    if not verifier.is_valid_request(request.data, request.headers):
        raise ValueError('Invalid request/credentials.')


def terra_is_broken(request: flask.Request):
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

    verify_signature(request)

    # Like /terraisbroken <argument>
    command_argument = request.form['text']
    return flask.escape("something")
