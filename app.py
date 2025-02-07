import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Marketo Webhook is Running!"

@app.route('/marketo-webhook', methods=['POST'])
def marketo_webhook():
    data = request.get_json()
    return jsonify({"message": "Webhook received!", "data": data})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
