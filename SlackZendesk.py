"""
Create a slack bot that uses the Zendesk api to retrieve the status of all tickets. If a ticket status is solved, use the slack api to delete the message sent by the zendesk app in a Channel with the ticket id.
"""

import os
import time
import json
import requests
import logging
import slack
from slack.errors import SlackApiError
from zendesk import Zendesk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Zendesk API
ZENDESK_SUBDOMAIN = os.environ.get('ZENDESK_SUBDOMAIN')
ZENDESK_USER = os.environ.get('ZENDESK_USER')
ZENDESK_TOKEN = os.environ.get('ZENDESK_TOKEN')

# Slack API
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')

# Zendesk API
zendesk = Zendesk(ZENDESK_SUBDOMAIN, ZENDESK_USER, ZENDESK_TOKEN)

# Slack API
client = slack.WebClient(token=SLACK_TOKEN)

while True:
    # Get all tickets
    tickets = zendesk.tickets_list()

    # Get all messages in the channel
    messages = client.conversations_history(channel=SLACK_CHANNEL)

    # Iterate through all tickets
    for ticket in tickets:
        # Get the ticket id
        ticket_id = ticket['id']
        # Get the ticket status
        ticket_status = ticket['status']
        # If the ticket status is solved
        if ticket_status == 'solved':
            # Iterate through all messages in the channel
            for message in messages['messages']:
                # Get the message text
                message_text = message['text']
                # If the message text contains the ticket id
                if str(ticket_id) in message_text:
                    # Get the message ts
                    message_ts = message['ts']
                    # Delete the message
                    client.chat_delete(channel=SLACK_CHANNEL, ts=message_ts)
