import os
import json
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenAI API Key from Heroku environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Marketo Webhook is Running!"

@app.route("/marketo-webhook", methods=["POST"])
def marketo_webhook():
    try:
        # Receive Lead Data from Marketo
        data = request.json
        first_name = data.get("firstName", "Unknown")
        last_name = data.get("lastName", "Unknown")
        company = data.get("company", "Unknown Company")
        email = data.get("email", "Unknown Email")

        # GPT Prompt for Enrichment
        prompt = f"""
        Given the following lead details:
        - First Name: {first_name}
        - Last Name: {last_name}
        - Company: {company}
        - Email: {email}

        Based on publicly available business intelligence, estimate:
        1. **Industry** (e.g., SaaS, Finance, Healthcare)
        2. **Company Size** (e.g., 1-10 employees, 11-50 employees)
        3. **Revenue Range** (e.g., $10M-$50M, $50M-$100M)
        4. **Company Fit Analysis**: A paragraph assessing if this company is a good fit for enterprise B2B software solutions.

        Respond **strictly in JSON format** with the following keys:
        - industry
        - company_size
        - revenue
        - company_fit
        """

        # Call OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI business analyst with expertise in lead enrichment."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract GPT Response
        gpt_response = response["choices"][0]["message"]["content"]
        enriched_data = json.loads(gpt_response)

        # Return Data to Marketo
        return jsonify({
            "success": True,
            "GPT_Industry": enriched_data.get("industry"),
            "GPT_Company_Size": enriched_data.get("company_size"),
            "GPT_Revenue": enriched_data.get("revenue"),
            "GPT_Company_Info": enriched_data.get("company_fit")
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
