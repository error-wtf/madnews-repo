
import subprocess, json, re, pathlib, textwrap

PROMPT_PATH = pathlib.Path(__file__).with_name("satire_prompt.txt")
BASE = PROMPT_PATH.read_text(encoding="utf-8").strip()
CTRL = re.compile(r"[\x00-\x1F\x7F-\x9F]")

def _clean(t:str)->str:
    return CTRL.sub("", t)

def generate_satire(headline:str)->str:
    prompt = f"{BASE}\n\nOriginalheadline: {headline}\n"
    try:
        proc = subprocess.run(
            ["ollama","run","--format","json","llama3",prompt],
            capture_output=True,text=True,encoding="utf-8",timeout=120
        )
        return json.loads(proc.stdout).get("response","").strip()
    except Exception:
        proc = subprocess.run(
            ["ollama","run","llama3",prompt],
            capture_output=True,text=True,encoding="utf-8",timeout=120
        )
        return _clean(proc.stdout).strip()
