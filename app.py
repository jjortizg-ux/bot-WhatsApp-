from flask import Flask, request
import requests, os

app = Flask(__name__)

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY = os.getenv("VERIFY_TOKEN", "mariquita123")

@app.route("/")
def home():
    return "Bot OK"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY:
        return request.args.get("hub.challenge")
    return "Error", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        value = data['entry'][0]['changes'][0]['value']
        if 'messages' in value:
            msg = value['messages'][0]
            from_number = msg['from']
            text = msg.get('text', {}).get('body', '')
            url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
            headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
            body = {"messaging_product": "whatsapp","to": from_number,"text": {"body": f"Hola! Soy tu bot de Mariquita 🤖 recibi: {text}"}}
            requests.post(url, json=body, headers=headers)
    except:
        pass
    return "ok", 200
