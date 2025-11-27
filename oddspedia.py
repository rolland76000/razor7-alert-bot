import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_latest_tip():
    """
    Récupère le dernier tip publié par Razor7 sur Oddspedia.
    Retourne (texte, lien) ou (None, None).
    """
    url = "https://oddspedia.com/tipsters/razor7"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    selectors = [
        "div.prediction-item",
        "div.tip-item",
        "article.prediction",
        ".prediction-list a",
        ".prediction-list .prediction-item"
    ]

    # On teste plusieurs sélecteurs (Oddspedia change souvent)
    for sel in selectors:
        el = soup.select_one(sel)
        if el:
            a = el.find("a", href=True)
            link = urljoin(url, a["href"]) if a else url
            text = el.get_text(separator=" ", strip=True)
            return text, link

    # fallback : chercher un lien /tips/
    a = soup.find("a", href=True)
    if a and "/tips/" in a["href"]:
        return a.get_text(strip=True), urljoin(url, a["href"])

    return None, None
