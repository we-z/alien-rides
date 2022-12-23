import json
from flask import Flask, request

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def handle_slack_event():
    # Parse the request data
    request_data = request.get_json()
    event_type = request_data["type"]
    event_data = request_data["event"]

    # If the event is a 'message.deleted' event, call the handle_message_deleted_event function
    if event_type == "message.deleted":
        handle_message_deleted_event(event_data)

    return "", 200

if __name__ == "__main__":
    app.run()
