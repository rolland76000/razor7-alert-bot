# check_tip.py
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Configuration via secrets / env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
RAZOR7_URL = os.getenv("RAZOR7_URL", "https://oddspedia.com/tipsters/razor7")
USER_AGENT = "Razor7AlertBot/1.0 (+mailto:ton_email@example.com)"

LAST_FILE = "last_seen.txt"
REQUEST_TIMEOUT = 15

def fetch_latest_tip():
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(RAZOR7_URL, headers=headers, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # plusieurs sélecteurs tentés (adaptable)
    selectors = [
        "div.prediction-item",
        "div.tip-item",
        "article.prediction",
        ".prediction-list a",
        ".prediction-list .prediction-item",
        ".tips-list a",
        ".tips-list .tip"
    ]
    for sel in selectors:
        el = soup.select_one(sel)
        if el:
            a = el.find("a", href=True)
            link = urljoin(RAZOR7_URL, a["href"]) if a else RAZOR7_URL
            # Compose an id: prefer href if present
            uid = a["href"] if a and a.get("href") else link
            text = el.get_text(separator=" ", strip=True)
            return uid.strip(), text, link

    # fallback simple : chercher premier lien contenant "/tips/"
    a = soup.find("a", href=True)
    if a and "/tips/" in a["href"]:
        link = urljoin(RAZOR7_URL, a["href"])
        uid = a["href"]
        text = a.get_text(strip=True) or "Nouveau tip (lien)"
        return uid.strip(), text, link

    return None, None, None

def read_last_seen():
    if os.path.exists(LAST_FILE):
        try:
            with open(LAST_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
        except:
            return None
    return None

def write_last_seen(uid):
    with open(LAST_FILE, "w", encoding="utf-8") as f:
        f.write(uid or "")

def send_telegram(message):
    if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
        print("Télégram non configuré (TELEGRAM_BOT_TOKEN/CHAT_ID manquants).")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "disable_web_page_preview": False}
    try:
        r = requests.post(url, data=payload, timeout=10)
        r.raise_for_status()
        return True
    except Exception as e:
        print("Erreur envoi Telegram:", e)
        return False

def main():
    try:
        uid, text, link = fetch_latest_tip()
    except Exception as e:
        print("Erreur fetch:", e)
        return 1

    if not uid:
        print("Aucun tip trouvé.")
        return 0

    last = read_last_seen()
    print("Dernier uid connu:", last)
    print("Uid trouvé:", uid)

    if uid != last:
        # nouveau tip
        msg = f"🆕 Nouveau tip Razor7 détecté :\n\n{text}\n\n🔗 {link}"
        ok = send_telegram(msg)
        print("Message envoyé:", ok)
        # mettre à jour le fichier local
        write_last_seen(uid)
    else:
        print("Pas de nouveau tip.")

    return 0

if __name__ == "__main__":
    main()
