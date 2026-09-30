import os
from flask import Flask, request
app = Flask(__name__)
@app.route("/")
def home():
    return "Christ The Rod Divine Tabernacle World Wide - LIVE! Rev 2:27 - Boima Musa Tamba"
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    msg = data.get("message","").lower()
    if "pit" in msg or "mining" in msg:
        return {"reply": "SAFE PIT: Benches 3m high 2m wide, Slope 45deg max, Haul Road 10m, Drainage 1m channel + sump. Stop July-August."}
    return {"reply": "Christ The Rod Assistant. Ask Mining, IT, Church, Sermon."}
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
