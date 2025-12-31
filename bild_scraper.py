
import requests
from bs4 import BeautifulSoup

def scrape_bild_headlines():
    url = "https://news.google.com/search?q=site:bild.de&hl=de&gl=DE&ceid=DE%3Ade"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')
        headlines = [h.text.strip() for h in soup.select("article h3") if h.text.strip()]
        if not headlines:
            raise Exception("Keine Headlines gefunden")
        return headlines
    except Exception as e:
        print("❗ FEHLER beim Scrapen, verwende Fallback-Headlines:", e)
        return [
            "Habeck warnt vor Heizkatastrophe",
            "Katze wird Bürgermeisterin von Wanne-Eickel",
            "Putin startet TikTok-Channel",
            "Scholz vergisst eigenen Namen",
            "Kanzleramt in Currywurst umbenannt"
        ]
