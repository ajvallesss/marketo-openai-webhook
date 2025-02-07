import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenAI API Key from Heroku config
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Marketo Webhook is Running!"

@app.route("/marketo-webhook", methods=["POST"])
def marketo_webhook():
    try:
        data = request.json

        first_name = data.get("First Name", "")
        last_name = data.get("Last Name", "")
        company_name = data.get("Company Name", "")
        email = data.get("Email Address", "")

        if not company_name:
            return jsonify({"error": "Missing Company Name"}), 400

        prompt = f"""
        Given the following company details:
        - Name: {company_name}
        - Person: {first_name} {last_name}
        - Email: {email}

        Please provide:
        - Industry
        - Estimated Company Size
        - Estimated Revenue
        - A short description of whether this company is a good fit.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are an expert in business insights and B2B sales."},
                      {"role": "user", "content": prompt}]
        )

        result = response["choices"][0]["message"]["content"]

        return jsonify({"GPT Response": result})

    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

if __name__ == "__main__":
    app.run(debug=True)
