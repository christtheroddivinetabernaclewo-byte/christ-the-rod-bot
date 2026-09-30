import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load knowledge
def load_knowledge():
    knowledge = ""
    for fname in ["01_Mining_Pit_Safety.txt", "02_IT_Services.txt", "03_Church_Ministry_Admin.txt", "04_Sermon_Scripture.txt"]:
        try:
            with open(fname, "r", encoding="utf-8", errors="ignore") as f:
                knowledge += f"\n---{fname}---\n" + f.read()
        except:
            pass
    return knowledge.lower()

KNOWLEDGE = load_knowledge()

@app.route("/")
def home():
    return """
<html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<style>body{font-family:Arial;background:#0f172a;color:white;text-align:center;padding:20px}
.box{background:white;color:#0f172a;padding:20px;border-radius:15px;max-width:500px;margin:auto}
input{width:80%;padding:12px;border-radius:10px;border:1px solid #ccc}
button{padding:12px 20px;background:#1e40af;color:white;border:none;border-radius:10px;margin-top:10px}
#reply{margin-top:20px;text-align:left;background:#f1f5f9;padding:15px;border-radius:10px;min-height:50px}
</style></head><body>
<h1>⚡ Christ The Rod Divine Tabernacle</h1>
<h3>World Wide AI Assistant</h3>
<p>Rev 2:27 - Rule with a Rod of Iron | Founder: Boima Musa Tamba</p>
<div class='box'>
<h3>Ask Me Anything:</h3>
<p style='font-size:13px'>Mining Pit Safety | IT Services | Church Admin | Sermon</p>
<input id='q' placeholder='Type e.g. how to make safe mining pit?'>
<br><button onclick='ask()'>Ask AI</button>
<div id='reply'>Your answer will appear here...</div>
</div>
<script>
async function ask(){
 let q=document.getElementById('q').value;
 document.getElementById('reply').innerText='Thinking...';
 let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q})});
 let j=await r.json();
 document.getElementById('reply').innerText=j.reply;
}
</script>
<p style='margin-top:20px;font-size:12px'>WhatsApp: +232... | Kono, Sierra Leone & Freetown</p>
</body></html>
"""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    msg = data.get("message","").lower()
    if not msg:
        return jsonify(reply="Ask me about Mining, IT, Church, Sermon.")
    # Simple search
    words = msg.split()
    best = ""
    # Check knowledge
    if any(w in msg for w in ["pit","mining","bench","slope","haul","drainage","kono","diamond","gold"]):
        best = "SAFE MINING PIT (Kono Standard): Benches 3m high x 2m wide, Slope max 45deg, Haul Road 10m wide, Drainage 1m channel + sump pump. Stop work July-August heavy rain. DANGER signs: cracks, water seepage, wall vertical >3m. Based on Boima Tamba mining engineer experience."
    elif any(w in msg for w in ["it","computer","network","website","whatsapp","virus","internet"]):
        best = "IT SERVICES: PC repair, Network setup, WhatsApp Business, Website design. Founder Boima - Computer Science. Pricing: Le 500,000 - Le 2,500,000. Freetown & Kono support."
    elif any(w in msg for w in ["church","admin","member","offering","tithe","tabernacle","pastor"]):
        best = "CHRIST THE ROD CHURCH ADMIN: Member registration, Offering records, Service schedule, Follow-up system. Revelation 2:27 leadership with Rod of Iron - love + discipline."
    elif any(w in msg for w in ["sermon","revelation","rod","iron","bible","preach"]):
        best = "Rev 2:27 KJV: And he shall rule them with a rod of iron. 3 Points: 1) Rod Given by Christ (Luke 10:19 Authority) 2) Rod Breaks Evil, not People 3) Rule with Wisdom & Love. Founder Boima Musa Tamba."
    else:
        best = f"You asked: '{msg}'. I have knowledge on: 1) Mining Pit Safety (Kono), 2) IT Services, 3) Church Ministry Admin, 4) Sermon on Rod of Iron. Ask specific question. Ministry: Christ The Rod Divine Tabernacle World Wide."
    return jsonify(reply=best)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
