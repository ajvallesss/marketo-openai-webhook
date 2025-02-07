from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Ensure OpenAI API key is loaded
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/marketo-webhook", methods=["POST"])
def marketo_webhook():
    try:
        # Check Content-Type Header
        if request.content_type != "application/json":
            return jsonify({"error": "Unsupported Media Type: Use 'application/json'"}), 415

        # Parse JSON Body
        data = request.get_json()
        if not data:
            return jsonify({"error": "400 Bad Request: No JSON payload received"}), 400
        
        # Extract Fields
        prompt = data.get("prompt")
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        email = data.get("email")
        title = data.get("title")
        company_name = data.get("companyName")

        if not prompt:
            return jsonify({"error": "Missing 'prompt' field"}), 400

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )

        generated_response = response["choices"][0]["message"]["content"]

        return jsonify({"response": generated_response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
