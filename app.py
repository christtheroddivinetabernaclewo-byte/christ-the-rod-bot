import os
from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

GROQ_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HTML = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Christ The Rod AI</title>
<style>body{background:#0a0e2a;color:white;font-family:sans-serif;text-align:center;padding:20px}.card{background:white;color:black;border-radius:20px;padding:20px;max-width:400px;margin:20px auto} button{padding:12px 20px;border-radius:20px;border:none;margin:5px;font-weight:bold}.ask{background:#2563eb;color:white}.voice{background:#ef4444;color:white}.read{background:#10b981;color:white} #ans{background:#f1f5f9;padding:15px;border-radius:12px;text-align:left;min-height:100px;margin-top:15px;white-space:pre-wrap}</style>
</head>
<body>
<h1>⚡ Christ The Rod<br>Divine Tabernacle</h1><p>Rev 2:27 - World Wide AI + Voice | Boima Musa Tamba</p>
<div class="card">
<h3>🎤 Ask by Voice or Text</h3>
<input id="q" placeholder="Ask anything..." style="width:90%;padding:12px;border-radius:20px;border:2px solid #2563eb"><br><br>
<button class="ask" onclick="ask()">💬 Ask AI</button>
<button class="voice" onclick="startVoice()">🎤 Voice</button>
<button class="read" onclick="readAns()">🔊 Read Answer</button>
<p style="font-size:12px;color:gray">Tap mic and speak</p>
<div id="ans">Ask me anything... quantum physics, mining, Bible, math...</div>
</div>
<script>
let lastAnswer="";
async function ask(){
 let qq=document.getElementById('q').value;
 if(!qq) return;
 document.getElementById('ans').innerText='Thinking...';
 let r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:qq})});
 let d=await r.json();
 lastAnswer=d.answer;
 document.getElementById('ans').innerText=d.answer;
}
function startVoice(){
 let rec=new(window.SpeechRecognition||window.webkitSpeechRecognition)();
 rec.lang='en-US'; rec.onresult=(e)=>{document.getElementById('q').value=e.results[0][0].transcript; ask();}; rec.start();
}
function readAns(){ if(!lastAnswer) return; let u=new SpeechSynthesisUtterance(lastAnswer); speechSynthesis.speak(u); }
</script>
</body>
</html>
"""

@app.route("/")
def home(): return render_template_string(HTML)

@app.route("/ask", methods=["POST"])
def ask_ai():
    data=request.get_json()
    q=data.get("question","")
    if not GROQ_KEY:
        return jsonify({"answer":"ERROR: GROQ_API_KEY not set in Render Environment. Add it."})
    try:
        payload={
            "model": "llama-3.1-8b-instant"
            "messages":[
                {"role":"system","content":"You are Christ The Rod Divine Tabernacle AI, assistant to Boima Musa Tamba. Expert in mining (Kono pits 3m bench 45deg), IT, Church Admin, Bible Rev 2:27, and general world knowledge. Answer clearly."},
                {"role":"user","content":q}
            ],
            "temperature":0.7
        }
        headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"}
        resp=requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        ans=resp.json()["choices"][0]["message"]["content"]
        return jsonify({"answer":ans})
    except Exception as e:
        return jsonify({"answer":f"Groq Error: {str(e)}"})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
