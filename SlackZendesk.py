import requests

# Replace SLACK_API_TOKEN and ZENDESK_API_TOKEN with your own API tokens
SLACK_API_TOKEN = "xoxb-your-slack-api-token"
ZENDESK_API_TOKEN = "your-zendesk-api-token"

# Set up a Slack event subscription for the 'message.deleted' event
SLACK_EVENT_SUBSCRIPTION_URL = "https://slack.com/api/events.subscribe"
payload = {
    "token": SLACK_API_TOKEN,
    "type": "message.deleted",
    "request_url": "http://your-server.com/slack/events",
}
headers = {
    "Content-Type": "application/json",
}
response = requests.post(SLACK_EVENT_SUBSCRIPTION_URL, json=payload, headers=headers)
if response.status_code != 200:
    raise Exception("Failed to set up event subscription")

# This function will be called whenever a message is deleted in a Slack channel
def handle_message_deleted_event(event_data):
    # Get the ticket ID from the message
    ticket_id = event_data["previous_message"]["text"]

    # Use the Zendesk API to retrieve the status of the ticket
    ZENDESK_API_URL = "https://your-zendesk-subdomain.zendesk.com/api/v2/tickets/{}.json"
    url = ZENDESK_API_URL.format(ticket_id)
    headers = {
        "Authorization": "Bearer {}".format(ZENDESK_API_TOKEN),
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to retrieve ticket status")
    ticket_status = response.json()["ticket"]["status"]

    # If the status of the ticket is "solved", delete the message in the Slack channel
    if ticket_status == "solved":
        # Use the Slack API to delete the message
        SLACK_API_URL = "https://slack.com/api/chat.delete"
        payload = {
            "token": SLACK_API_TOKEN,
            "channel": event
