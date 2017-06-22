import requests
from flask import Flask, request
import os
import json
import sys
from conf import Config as config


app = Flask(__name__)

def message_text(_text):
    return {"text": _text}


def quick_replies():
    replies_quick = {
        "text": "Pick a color:",
        "quick_replies": [
            {
                "content_type": "text",
                "title": "Red",
                "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
            },
            {
                "content_type": "text",
                "title": "Green",
                "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
            }
        ]
    }
    return {"message": replies_quick}


def sender_action():
    return {"sender_action": "typing_on"}


def button_template(_payload="-!-"):
    template_button = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "What do you want to do next?",
                "buttons": [
                    {
                        "type": "web_url",
                        "url": "https://petersapparel.parseapp.com",
                        "title": "Show Website"
                    },
                    {
                        "type": "postback",
                        "title": "Start Chatting",
                        "payload": _payload
                    }
                ]
            }
        }
    }
    return {"message": template_button}


def generic_template():
    template_generic = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Welcome to Peter\'s Hats",
                        "image_url": "https://petersfancybrownhats.com/company_image.png",
                        "subtitle": "We\'ve got the right hat for everyone.",
                        "default_action": {
                            "type": "web_url",
                            "url": "https://peterssendreceiveapp.ngrok.io/view?item=103",
                            "messenger_extensions": True,
                            "webview_height_ratio": "tall",
                            "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                        },
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": "https://petersfancybrownhats.com",
                                "title": "View Website"
                            }, {
                                "type": "postback",
                                "title": "Start Chatting",
                                "payload": "DEVELOPER_DEFINED_PAYLOAD"
                            }
                        ]
                    }
                ]
            }
        }
    }
    return {"message": template_generic}


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "VERIFY_TOKEN-#33#":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    # log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    # the facebook ID of the person sending you the message
                    sender_id = messaging_event["sender"]["id"]
                    # the recipient's ID, which should be your page's facebook ID
                    recipient_id = messaging_event["recipient"]["id"]
                    # the message's text
                    # text_message = messaging_event["message"]["text"]

                    send_message(sender_id, quick_replies())
                    # send_message(sender_id,generic_template())

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    sender_id = messaging_event["sender"]["id"]
                    text_message = messaging_event["postback"]["payload"]
                    send_message(sender_id, message_text(text_message))

    return "ok", 200


def send_message(recipient_id, functionMessage):

    log("sending message to {recipient}: {text}".format(
        recipient=recipient_id, text=functionMessage))

    params = {
        "access_token": config.FBAPI_APP_SECRET
    }
    headers = {
        "Content-Type": "application/json"
    }
    _data = {"recipient": {"id": recipient_id}}
    _data.update(functionMessage)
    data = json.dumps(_data)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
    log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run()
