import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_latest_tip():
    """
    Retourne (text, link) du dernier tip Razor7, ou (None, None).
    """
    url = "https://oddspedia.com/tipsters/razor7"
    headers = {"User-Agent": "Mozilla/5.0 (compatible)"}
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
    for sel in selectors:
        el = soup.select_one(sel)
        if el:
            a = el.find("a", href=True)
            link = urljoin(url, a["href"]) if a else url
            text = el.get_text(separator=" ", strip=True)
            return text, link

    a = soup.find("a", href=True)
    if a and "/tips/" in a["href"]:
        return a.get_text(strip=True), urljoin(url, a["href"])

    return None, None
