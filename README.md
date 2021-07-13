# pagerduty-trigger-slack-command

A python script that uses the [PagerDuty V2 Events API](https://developer.pagerduty.com/docs/events-api-v2/overview/) to trigger an incident in the [Broad PagerDuty account](https://broadinstitute.pagerduty.com/) for a Terra outage. This enables any member of the DSP community to page the Terra on-call engineer in the event that they discover an outage.

This script runs in a Google Cloud Function (https://us-central1-dsp-devops.cloudfunctions.net/pagerduty-slack-trigger-fn) and is triggerable from the broadinstitute slack via the "Trigger Terra Incident" slack app.

<sub>This project was created as part of the 2021 DSP Code Jamboree.</sub>

## How to trigger

Type `/terraisdown` in the broadinstitute slack. Briefly describe what is wrong in text, and then press enter. This will generate an incident for the [Manually Triggered Terra Incident service](https://broadinstitute.pagerduty.com/service-directory/PUB2AMR) and return an incident key, which is a uuid for the incident. 
