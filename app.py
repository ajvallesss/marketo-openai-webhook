import os
import openai
import json
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Fetch OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set it in your environment variables.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route("/", methods=["GET"])
def home():
    return "Marketo Webhook is Running!", 200

@app.route("/marketo-webhook", methods=["POST"])
def marketo_webhook():
    try:
        # Parse incoming JSON data
        data = request.get_json()
        first_name = data.get("First Name", "")
        last_name = data.get("Last Name", "")
        company_name = data.get("Company Name", "")
        email = data.get("Email Address", "")

        if not company_name:
            return jsonify({"error": "Company Name is required"}), 400

        # OpenAI Prompt for GPT enrichment
        prompt = f"""
        Given the following person:
        - Name: {first_name} {last_name}
        - Email: {email}
        - Company: {company_name}

        Please provide:
        1. The industry this company operates in.
        2. The estimated company size (small, medium, or large).
        3. Estimated annual revenue.
        4. A brief description assessing whether this company is a good fit for B2B SaaS solutions.
        """

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract GPT response
        gpt_response = response.choices[0].message.content.strip()

        return jsonify({
            "GPT Industry": gpt_response.split("\n")[0],
            "GPT Company Size": gpt_response.split("\n")[1],
            "GPT Revenue": gpt_response.split("\n")[2],
            "GPT Company Info": gpt_response.split("\n")[3]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
