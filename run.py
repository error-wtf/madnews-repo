"""
run.py – fetch → satire → HTML
--------------------------------
• holt bis zu 30 BILD-Headlines (fetch_rss.py)
• generiert pro Headline einen validierten Satire-Block
• schreibt alles in docs/index.html (Basis-Template hart codiert)
"""

from pathlib import Path
from datetime import datetime as dt

from fetch_rss import fetch_bild_headlines      # unverändert
from twist_with_model import generate_satire

MAX_ITEMS = 30
OUT_FILE   = Path("docs/index.html")

print("📰  Hole BILD-Headlines …")
headline_list = fetch_bild_headlines(max_items=30)
print(f"→ {len(headline_list)} Headlines gefunden\n")

satire_blocks: list[str] = []

print("🤖  Generiere Satire mit DeepSeek …")
for idx, head in enumerate(headline_list, start=1):
    print(f"  {idx}/{len(headline_list):<d}  {head[:55]:.<55}", end=" ", flush=True)
    block = generate_satire(head)
    if block:
        satire_blocks.append(block)
        print("✅")
    else:
        print("⏭️  übersprungen")

if not satire_blocks:
    raise SystemExit("❌  Kein einziger valider Satire-Block erzeugt – Abbruch.")

# ----------  HTML schreiben  ----------------------------
html_body = "\n\n<hr/>\n\n".join(
    f"<p>{b.replace(chr(10), '<br/>')}</p>" for b in satire_blocks
)

html_full = f"""<!DOCTYPE html>
<meta charset="utf-8">
<title>MAD NEWS</title>
<h1>MAD NEWS</h1>
{html_body}
<hr/>
<small>Stand: {dt.now():%d.%m.%Y %H:%M:%S}</small>
"""

OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUT_FILE.write_text(html_full, encoding="utf-8")
print(f"\n✅  Ausgabe gespeichert: {OUT_FILE}")

