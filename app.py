from flask import Flask, request
import requests, os

app = Flask(__name__)

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY = os.getenv("VERIFY_TOKEN", "bot123")

@app.route("/")
def home():
    return "Bot OK"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY:
            return challenge, 200
        return "Error token", 403

    if request.method == "POST":
        data = request.get_json()
        try:
            value = data['entry'][0]['changes'][0]['value']
            if 'messages' in value:
                msg = value['messages'][0]
                sender = msg['from']
                text = msg.get('text', {}).get('body', '')

                # Aquí responde el bot
                url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
                headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
                payload = {
                    "messaging_product": "whatsapp",
                    "to": sender,
                    "text": {"body": f"Hola! Recibi: {text}"}
                }
                requests.post(url, json=payload, headers=headers)
        except Exception as e:
            print(f"Error: {e}")
        return "OK", 200
