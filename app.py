import os
import openai
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load OpenAI API Key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY is missing. Check your Heroku config vars.")

client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Ensure no 'proxies=' argument

@app.route("/", methods=["GET"])
def home():
    return "Marketo OpenAI Webhook is running!", 200

@app.route("/marketo-webhook", methods=["POST"])
def marketo_webhook():
    try:
        data = request.json
        prompt = data.get("prompt", "Tell me something interesting about AI.")
        
        response = client.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return jsonify({"response": response.choices[0].message["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
