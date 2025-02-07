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
        Based on the company name "{company_name}", provide the following information:
        - Industry
        - Estimated Company Size
        - Estimated Revenue
        - Brief paragraph evaluating if they are a good fit for a B2B SaaS product.

        Use public knowledge, educated estimates, and business logic.
        """

        # Call OpenAI API
        client = openai.OpenAI()  # Using OpenAI v1.0+ syntax
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )

        # Extract GPT response
        gpt_output = response.choices[0].message.content.strip()

        # Format response
        result = {
            "GPT Industry": gpt_output.split("\n")[0] if len(gpt_output.split("\n")) > 0 else "",
            "GPT Company Size": gpt_output.split("\n")[1] if len(gpt_output.split("\n")) > 1 else "",
            "GPT Revenue": gpt_output.split("\n")[2] if len(gpt_output.split("\n")) > 2 else "",
            "GPT Company Info": "\n".join(gpt_output.split("\n")[3:]) if len(gpt_output.split("\n")) > 3 else ""
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
