import os
import json
from flask import Flask, request, jsonify
import openai

# Load OpenAI API Key from Heroku environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key!")

# Initialize OpenAI client with the latest format
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Flask app setup
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Marketo OpenAI Webhook is running!", 200

@app.route("/marketo-webhook", methods=["POST"])
def marketo_webhook():
    try:
        data = request.get_json()

        # Extract user input
        first_name = data.get("First Name", "User")
        last_name = data.get("Last Name", "")
        company = data.get("Company Name", "Unknown Company")
        email = data.get("Email Address", "")

        # OpenAI API call
        prompt = f"Generate a professional follow-up email for {first_name} {last_name} from {company}."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return jsonify({"success": True, "message": response.choices[0].message.content}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
