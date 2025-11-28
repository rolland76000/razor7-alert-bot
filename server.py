# server.py
import time
import threading
import requests
from oddspedia import fetch_latest_tip
import os
from flask import Flask, jsonify

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
RAZOR7_URL = os.environ.get("RAZOR7_URL", "https://oddspedia.com/tipsters/razor7")
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", "60"))

last_tip_id = None
app = Flask(__name__)

def send_telegram(text):
    if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
        print("Telegram variables missing; skip sending.")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": False
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        r.raise_for_status()
        return True
    except Exception as e:
        print("Erreur envoi Telegram:", e)
        return False

def monitor_loop():
    global last_tip_id
    print("Démarrage du monitor Razor7 (background thread).")
    while True:
        try:
            text, link = fetch_latest_tip()
            if text:
                uid = link or text
                if uid != last_tip_id:
                    last_tip_id = uid
                    msg = f"🆕 Nouveau tip Razor7 :\n\n{text}\n\n🔗 {link}"
                    print("Envoi message:", msg)
                    send_telegram(msg)
                else:
                    print("Aucun nouveau tip.")
            else:
                print("Aucun tip trouvé (sélecteur à vérifier).")
        except Exception as e:
            print("Erreur surveillance:", e)
        time.sleep(CHECK_INTERVAL)

@app.route("/")
def status():
    return jsonify({
        "status": "ok",
        "service": "razor7-alert-bot",
        "last_tip": bool(last_tip_id)
    })

def start_background_thread():
    thread = threading.Thread(target=monitor_loop, daemon=True)
    thread.start()

if __name__ == "__main__":
    start_background_thread()
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
