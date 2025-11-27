import time
import requests
from oddspedia import fetch_latest_tip
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, CHECK_INTERVAL

last_tip_id = None

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_web_page_preview": False,
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print("Erreur Telegram:", e)

def monitor():
    global last_tip_id
    print("Bot Razor7 lancé.")
    while True:
        try:
            text, link = fetch_latest_tip()
            if text:
                uid = link or text  # anti doublon simple
                if uid != last_tip_id:
                    last_tip_id = uid
                    msg = f"🆕 Nouveau tip Razor7 :\n\n{text}\n\n🔗 {link}"
                    send_telegram(msg)
                else:
                    print("Aucun nouveau tip.")
        except Exception as e:
            print("Erreur:", e)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor()
