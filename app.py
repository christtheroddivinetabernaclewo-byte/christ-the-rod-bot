import os, requests
from flask import Flask, request, jsonify

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "") # You will add free key later

def load_knowledge():
    k = ""
    for fname in ["01_Mining_Pit_Safety.txt","02_IT_Services.txt","03_Church_Ministry_Admin.txt","04_Sermon_Scripture.txt"]:
        try:
            with open(fname,"r",encoding="utf-8",errors="ignore") as f: k+=f.read()+"\n"
        except: pass
    return k

KNOWLEDGE = load_knowledge()

def ask_general_ai(question):
    # If you have GROQ key, it answers like ChatGPT
    if GROQ_API_KEY:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"},
                json={"model":"llama-3.1-8b-instant","messages":[
                    {"role":"system","content": f"You are Christ The Rod AI by Boima Musa Tamba. Knowledge: {KNOWLEDGE[:3000]}. Rev 2:27. Answer helpfully, blend local knowledge + general knowledge. Founder Boima."},
                    {"role":"user","content": question}]}, timeout=15)
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(e)
    # Free fallback without API key - general knowledge mode
    return f"GENERAL KNOWLEDGE (Christ The Rod AI): You asked '{question}'. As Boima Musa Tamba's assistant, I know: Mining (Kono pits 3m bench, 45deg slope), IT, Church Admin, and Bible Rev 2:27. For deeper general knowledge like history/science/math, add free GROQ API key in Render Environment. Meanwhile I can reason: {question} -> Let me help with practical wisdom from my knowledge base + general principles. [Enable GROQ for full ChatGPT-like power]"

@app.route("/")
def home():
    return """
<html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<style>
body{font-family:Arial;background:#0f172a;color:white;text-align:center;padding:15px}
.box{background:white;color:#0f172a;padding:20px;border-radius:20px;max-width:550px;margin:auto;box-shadow:0 10px 30px rgba(0,0,0,0.3)}
input{width:70%;padding:14px;border-radius:30px;border:2px solid #1e40af;font-size:16px}
button{padding:14px 18px;border:none;border-radius:30px;margin:5px;font-weight:bold;cursor:pointer}
.blue{background:#1e40af;color:white}.red{background:#ef4444;color:white}.green{background:#10b981;color:white}
#reply{margin-top:15px;text-align:left;background:#f1f5f9;padding:15px;border-radius:15px;min-height:80px;white-space:pre-wrap}
.mic-active{background:orange!important;animation:pulse 1s infinite}
@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.1)}100%{transform:scale(1)}}
</style></head><body>
<h1>⚡ Christ The Rod Divine Tabernacle</h1>
<p>Rev 2:27 - World Wide AI + Voice | Boima Musa Tamba</p>
<div class='box'>
<h3>🎤 Ask by Voice or Text</h3>
<input id='q' placeholder='Ask anything... e.g. What is photosynthesis?'>
<br>
<button class='blue' onclick='ask()'>💬 Ask AI</button>
<button class='red' id='micBtn' onclick='startVoice()'>🎤 Voice</button>
<button class='green' onclick='speakLast()'>🔊 Read Answer</button>
<div id='status' style='font-size:12px;color:gray;margin-top:5px'>Tap mic and speak</div>
<div id='reply'>Welcome! I can now answer GENERAL KNOWLEDGE like Meta AI + your Mining/Church knowledge. Try voice!</div>
</div>
<script>
let lastAnswer='';
let recognition;
function ask(){
 let q=document.getElementById('q').value;
 if(!q) return;
 document.getElementById('reply').innerText='Thinking... AI is reasoning...';
 fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q})})
.then(r=>r.json()).then(j=>{
   lastAnswer=j.reply;
   document.getElementById('reply').innerText=j.reply;
   speak(j.reply);
 });
}
function startVoice(){
 if(!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)){alert('Use Chrome browser for voice');return;}
 const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 recognition=new SR(); recognition.lang='en-US';
 recognition.start();
 document.getElementById('micBtn').classList.add('mic-active');
 document.getElementById('status').innerText='🎧 Listening... speak now!';
 recognition.onresult=function(e){
   let text=e.results[0][0].transcript;
   document.getElementById('q').value=text;
   document.getElementById('status').innerText='Heard: '+text;
   ask();
 };
 recognition.onend=()=>{document.getElementById('micBtn').classList.remove('mic-active');};
}
function speak(text){
 if('speechSynthesis' in window){
   window.speechSynthesis.cancel();
   let u=new SpeechSynthesisUtterance(text.substring(0,300));
   u.rate=0.95; window.speechSynthesis.speak(u);
 }
}
function speakLast(){if(lastAnswer) speak(lastAnswer);}
document.getElementById('q').addEventListener('keypress',function(e){if(e.key==='Enter') ask();});
</script>
</body></html>
"""

@app.route("/chat", methods=["POST"])
def chat():
    msg = (request.get_json() or {}).get("message","")
    if not msg: return jsonify(reply="Ask anything!")
    # If question matches your files, use local, else use general AI
    lower = msg.lower()
    if any(w in lower for w in ["pit","mining","kono","bench","slope"]):
        return jsonify(reply="MINING (Your Expert): 3m high benches, 2m wide, 45deg slope, 10m haul road, drainage channel 1m. Stop July-Aug rain. Danger: cracks/water.")
    # General knowledge for everything else
    ans = ask_general_ai(msg)
    return jsonify(reply=ans)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
