from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI API Key (Heroku will store this securely)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/marketo-webhook', methods=['POST'])
def marketo_webhook():
    data = request.json

    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    email = data.get("email", "")
    company = data.get("company", "")

    # Construct OpenAI prompt
    prompt = f"""
    Investigate the following lead:
    - Name: {first_name} {last_name}
    - Email: {email}
    - Company: {company}
    
    Provide:
    1. The company's industry
    2. Company size (small, mid, enterprise)
    3. Approximate revenue range
    4. A brief paragraph assessing if this company is a good fit for enterprise solutions.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You enrich marketing lead data."},
                      {"role": "user", "content": prompt}],
            api_key=OPENAI_API_KEY
        )

        response_text = response['choices'][0]['message']['content']
        lines = response_text.split("\n")

        industry = lines[0].split(": ")[1] if len(lines) > 0 else "Unknown"
        company_size = lines[1].split(": ")[1] if len(lines) > 1 else "Unknown"
        revenue = lines[2].split(": ")[1] if len(lines) > 2 else "Unknown"
        fit_assessment = " ".join(lines[3:]) if len(lines) > 3 else "No assessment available."

        return jsonify({
            "GPT_Industry": industry,
            "GPT_Company_Size": company_size,
            "GPT_Revenue": revenue,
            "GPT_Fit_Assessment": fit_assessment
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
