import os
from flask import Flask, request, jsonify
import openai

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set the 'OPENAI_API_KEY' environment variable.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Marketo OpenAI Webhook is running!"})

@app.route("/marketo-webhook", methods=["POST"])
def marketo_webhook():
    try:
        data = request.json
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400

        response = client.completions.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=100
        )

        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
