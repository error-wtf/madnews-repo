
from fetch_rss import fetch_bild_rss_headlines
from twist_with_ollama import twist_headline
import os
import json

os.makedirs("docs", exist_ok=True)
output = []

print("📰 Lade BILD-Schlagzeilen (Original RSS)...")
try:
    headlines = fetch_bild_rss_headlines()
except Exception as e:
    print("❗ FEHLER beim Scrapen, verwende Fallback-Headlines:", e)
    headlines = [
        "Mann isst 42 Currywürste – Weltrekord oder Wahnsinn?",
        "Katzen übernehmen Bundestag",
        "Olaf Scholz erklärt Montag für abgeschafft",
        "Neue Partei fordert: Gratis Pommes für alle",
        "Wissenschaftler entdecken, dass Kaffee denken kann"
    ]

print("🔍 Gefundene Headlines:", headlines)

print("🤖 Generiere Satire mit Ollama...")
for i, headline in enumerate(headlines, 1):
    satire = twist_headline(headline)
    print(f"{i}. {headline} -> {satire[:80]}...")
    output.append({"original": headline, "satire": satire})

with open("docs/index.html", "w") as f:
    f.write("<html><body><h1>MAD NEWS – BILD RSS Satire</h1><ul>")
    for item in output:
        f.write(f"<li><strong>{item['original']}</strong><br><em>{item['satire']}</em></li>")
    f.write("</ul></body></html>")

with open("docs/news.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ Fertig! Ausgabe gespeichert in docs/")
