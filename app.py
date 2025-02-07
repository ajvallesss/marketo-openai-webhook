import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ensure OpenAI API Key is set in Heroku config vars
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Marketo Webhook is Running!", 200

@app.route("/marketo-webhook", methods=["POST"])
def marketo_webhook():
    data = request.json
    
    first_name = data.get("First Name", "")
    last_name = data.get("Last Name", "")
    company_name = data.get("Company Name", "")
    email = data.get("Email Address", "")

    # Constructing the prompt
    prompt = f"""
    Given the following lead information:

    - Name: {first_name} {last_name}
    - Company: {company_name}
    - Email: {email}

    Please determine:
    1. Industry
    2. Company Size
    3. Revenue Estimate
    4. A short paragraph on whether this company is a good fit.

    Respond in **JSON format** with fields:
    - GPT_Industry
    - GPT_Company_Size
    - GPT_Revenue
    - GPT_Company_Info
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a B2B business analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        gpt_output = response.choices[0].message.content

        return jsonify({"success": True, "GPT_Response": gpt_output})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
