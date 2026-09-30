from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GROQ_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/")
def home():
    return """
    <html>
    <head><title>Christ The Rod Bot</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body style="font-family:Arial; text-align:center; padding:20px; background:#f5f5f5;">
    <h1 style="color:#2c3e50;">Christ The Rod Bot</h1>
    <h3>World Wide AI + Voice | Rev 2:27</h3>
    <p>Powerful Ministry Tool - LIVE!</p>
    <div style="background:white; padding:20px; border-radius:10px; max-width:500px; margin:auto;">
    <input id="msg" placeholder="Ask about scripture..." style="width:70%; padding:12px; border-radius:5px; border:1px solid #ccc;">
    <button onclick="send()" style="padding:12px 20px; background:#2c3e50; color:white; border:none; border-radius:5px;">Send</button>
    <div id="reply" style="margin-top:20px; text-align:left; white-space:pre-wrap;"></div>
    </div>
    <script>
    async function send(){
     let m=document.getElementById('msg').value;
     document.getElementById('reply').innerText='Praying...';
     let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});
     let d=await r.json();
     document.getElementById('reply').innerText=d.reply;
    }
    </script>
    </body></html>
    """

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are Christ The Rod Bot, World Wide AI + Voice, ministry assistant for Christ The Rod Divine Tabernacle. Answer with wisdom, power, scripture. Rev 2:27"},
            {"role": "user", "content": user_message}
        ]
    }
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=20)
        result = response.json()
        bot_reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)} - Please check GROQ_API_KEY in Render Environment"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
