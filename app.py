from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route("/marketo-webhook", methods=["POST"])
def marketo_webhook():
    try:
        print("Received request headers:", request.headers)  # Debugging: Show headers
        print("Received request body:", request.data.decode("utf-8"))  # Debugging: Show raw body

        # Ensure request is JSON
        if not request.is_json:
            return jsonify({"error": "415 Unsupported Media Type: Request must be JSON"}), 415

        data = request.get_json()

        # Debugging: Log parsed JSON data
        print("Parsed JSON data:", data)

        # Check if 'prompt' exists
        if "prompt" not in data:
            return jsonify({"error": "Missing prompt"}), 400

        # Generate OpenAI response
        response = client.completions.create(
            model="gpt-4",
            prompt=data["prompt"],
            max_tokens=100
        )

        return jsonify({"response": response.choices[0].text.strip()})

    except Exception as e:
        print("Error occurred:", str(e))  # Debugging: Log error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
