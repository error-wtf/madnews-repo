"""
twist_with_model.py
───────────────────
  • Holt einen einzelnen BILD-Titel ab
  • Ruft Ollama (lokal!) mit llama3:latest auf
  • Liefert (Headline, Artikel) als HTML-String

Robust gegen
  – <think>-Blöcke
  – Gedankliche Vorreden des Modells
  – Zu viele/zu wenige Absatzblöcke
"""

import json
import textwrap
import time
import re
import requests

# ----------------------------- Konfiguration -----------------------------

OLLAMA_URL  = "http://localhost:11434/api/generate"   # nur lokal!
MODEL       = "llama3:latest"
TIMEOUT_S   = 120                      # HTTP-Timeout
MAX_TOKENS  = 512                      # weniger = schneller, stabiler
STOP_TOKENS = ["</"]                   # <think> bleiben optional

# ------------------------------------------------------------------------

PROMPT_TEMPLATE = textwrap.dedent("""
# Satire-Generator MAD NEWS

**Aufgabe**: Ersetze die gegebene BILD-Schlagzeile durch:
- Eine neue satirische Headline (ohne Sternchen)
- Einen bissigen, gewaltfreien Artikel (150–250 Wörter, deutsch)

**Format GENAU einhalten**  
1️⃣ Erste Zeile: Nur die neue Headline  
2️⃣ Eine Leerzeile  
3️⃣ Artikel-Text (keine Zusätze, kein Wort 'Leerzeile')

Beispiel:
CDU will Einheitsfarbe Grau – Antifa verteilt Regenbogenkonfetti

Nachfolgend die echte Vorlage ↓
------------------------------------------------------------
ORIGINAL : {headline}
------------------------------------------------------------
""").strip()


def _call_llm(prompt: str) -> str:
    """Sendet Prompt an Ollama, liefert die gesamte Antwort."""
    payload = dict(
        model       = MODEL,
        prompt      = prompt,
        temperature = 0.7,
        max_tokens  = MAX_TOKENS,
        stop        = STOP_TOKENS,
        stream      = False
    )
    r = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT_S)
    r.raise_for_status()
    return r.json()["response"].strip()


def _split_blocks(raw: str) -> tuple[str, str]:
    """
    ▸ Entfernt optionalen <think> … </think>
    ▸ Trennt Headline + Artikel (zwei Blöcke)
    ▸ Wirft Fehlermeldung bei Problemen
    """
    txt = raw.lstrip()

    # 1) <think>-Block entfernen
    if txt.lower().startswith("<think"):  # auf <think> prüfen
        end = txt.lower().find("</think>")
        if end != -1:
            txt = txt[end + len("</think>") :].lstrip()
        else:
            # kein schließender Tag → alles vor erster Leerzeile kappen
            txt = txt.split("\n\n", 1)[1].lstrip() if "\n\n" in txt else txt

    # 2) Headline / Artikel trennen (per erster Leerzeile)
    parts = [p.strip() for p in txt.split("\n\n", 1) if p.strip()]
    if len(parts) != 2:
        raise ValueError("Modell-Ausgabe hatte nicht genau 2 Blöcke:", raw)
    return parts[0], parts[1]


# ------------------------ Öffentlich genutzte Funktion -------------------

def generate_satire(orig_headline: str) -> str:
    """
    Liefert ein fertiges HTML-Snippet (fettierte Headline + Artikel).
    """
    # Prompt bauen (Original in einfache Anführungszeichen)
    prompt = PROMPT_TEMPLATE.format(headline=orig_headline.replace('"', "'"))
    raw    = _call_llm(prompt)
    head, article = _split_blocks(raw)

    # Sternchen aus Headline entfernen und trim
    clean_head = re.sub(r"\*", "", head).strip()

    # HTML-Ausgabe: fette Headline + Artikel, mit genau einer Leerzeile dazwischen
    html = f"<b>{clean_head}</b>\n\n{article}"
    return html


# ---------------------------- Schnelltest --------------------------------
if __name__ == "__main__":
    TEST = "Zoff um Mullah-Angriff – Trump zickt aus!"
    print(generate_satire(TEST))

