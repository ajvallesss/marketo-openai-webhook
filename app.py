import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/marketo-webhook", methods=["POST"])
def marketo_webhook():
    try:
        data = request.json
        first_name = data.get("First Name", "")
        last_name = data.get("Last Name", "")
        company_name = data.get("Company Name", "")
        email = data.get("Email Address", "")

        # Construct the query for GPT
        prompt = f"""
        Provide a business overview for {company_name}. 
        Include details about its industry, estimated company size, and revenue. 
        Also, determine if the company is a good fit for our services.
        """

        # Use the updated OpenAI API syntax
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract response text
        gpt_response = response["choices"][0]["message"]["content"]

        return jsonify({
            "GPT Industry": "Extract industry from response",  
            "GPT Company Size": "Extract company size from response",  
            "GPT Revenue": "Extract revenue from response",  
            "GPT Company Info": gpt_response,
            "success": True
        })

    except Exception as e:
        return jsonify({"error": str(e), "success": False})

if __name__ == "__main__":
    app.run(debug=True)
