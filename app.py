import os
import openai
from flask import Flask, request, jsonify

# Initialize Flask App
app = Flask(__name__)

# OpenAI API Key (Make sure it's set in Heroku config vars)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Marketo Webhook is Running!"

@app.route("/marketo-webhook", methods=["POST"])
def marketo_webhook():
    try:
        # Get JSON payload from Marketo webhook
        data = request.get_json()
        
        first_name = data.get("First Name", "")
        last_name = data.get("Last Name", "")
        company_name = data.get("Company Name", "")
        email = data.get("Email Address", "")

        if not company_name or not email:
            return jsonify({"error": "Missing required fields"}), 400

        # Create a prompt for GPT-4 to enrich company data
        prompt = f"""
        Provide insights for the company "{company_name}":
        1. Industry:
        2. Estimated Company Size:
        3. Estimated Revenue:
        4. Brief analysis on whether they are a good fit for a B2B SaaS product.
        """

        # Call OpenAI API (Updated for v1.0+)
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": prompt}]
        )

        # Extract GPT response
        gpt_output = response.choices[0].message.content.strip().split("\n")

        # Format response
        result = {
            "GPT Industry": gpt_output[0].replace("1. Industry:", "").strip() if len(gpt_output) > 0 else "",
            "GPT Company Size": gpt_output[1].replace("2. Estimated Company Size:", "").strip() if len(gpt_output) > 1 else "",
            "GPT Revenue": gpt_output[2].replace("3. Estimated Revenue:", "").strip() if len(gpt_output) > 2 else "",
            "GPT Company Info": "\n".join(gpt_output[3:]).replace("4. Brief analysis on whether they are a good fit for a B2B SaaS product:", "").strip() if len(gpt_output) > 3 else ""
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
