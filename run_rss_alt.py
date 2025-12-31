
from fetch_rss import fetch_bild_rss_headlines
from twist_with_ollama import twist_headline
import os
import json

os.makedirs("docs", exist_ok=True)
output = []

print("📰 Lade BILD-Schlagzeilen (via rss-verzeichnis.de)...")
try:
    headlines = fetch_bild_rss_headlines()
except Exception as e:
    print("❗ FEHLER beim Scrapen, verwende Fallback-Headlines:", e)
    headlines = [
        "Kuh fliegt durch Windschutzscheibe – Fahrer unverletzt",
        "Wissenschaftler entdecken drittes Bein im Bundestag",
        "Berliner demonstrieren für mehr Stulle auf Rezept",
        "Angela Merkel übernimmt TikTok-Kanal von Putin",
        "Neuer Feiertag für Menschen, die nie Feierabend machen"
    ]

print("🔍 Gefundene Headlines:", headlines)

print("🤖 Generiere Satire mit Ollama...")
for i, headline in enumerate(headlines[:5], 1):
    satire = twist_headline(headline)
    print(f"{i}. {headline} -> {satire[:80]}...")
    output.append({"original": headline, "satire": satire})

with open("docs/index.html", "w") as f:
    f.write("<html><body><h1>MAD NEWS – BILD RSS (Alternativ)</h1><ul>")
    for item in output:
        f.write(f"<li><strong>{item['original']}</strong><br><em>{item['satire']}</em></li>")
    f.write("</ul></body></html>")

with open("docs/news.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ Fertig! Ausgabe gespeichert in docs/")
