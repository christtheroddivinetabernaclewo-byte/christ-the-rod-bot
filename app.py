from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

GROQ_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are Christ The Rod Bot - World Wide AI + Voice, a powerful ministry assistant for Christ The Rod Divine Tabernacle. Answer with wisdom, power, and scripture. Rev 2:27"
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        result = response.json()
        bot_reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)} - Check API Key"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
