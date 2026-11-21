"""Namluvení textů přes API ElevenLabs podle fronty fronta.json (spouští workflow „Namluvit“).

fronta.json:
  {"ulohy": [
    {"jazyk": "es", "text": "Naučná videa/spanelske-texty-01-08.md", "sekce": "07",
     "vystup": "Naučná videa/07-nase-nic-neni-dukaz/zvuk/voz-ES.mp3"}
  ]}
  text   – soubor s textem (cesta od kořene repa); se „sekce“ se vezme první blok ``` pod nadpisem „## <sekce>…“
  vystup – kam uložit MP3 (jen uvnitř „Naučná videa/“); vedle vznikne <název>.casy.json s časy písmen
  znovu  – true = namluvit i když MP3 už existuje (jinak se úloha přeskočí)

Hotové úlohy z fronty zmizí, nepovedené v ní zůstanou. Záznam posledního běhu je ve vysledek.md.
Hlasy a nastavení: hlasy.json. Klíč: proměnná ELEVENLABS_API_KEY (v GitHubu tajemství).
Jen standardní knihovna Pythonu."""
import base64, datetime, json, os, re, sys, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("REPO_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
API = os.environ.get("ELEVENLABS_API_BASE", "https://api.elevenlabs.io")
FRONTA = os.environ.get("FRONTA") or os.path.join(HERE, "fronta.json")
VYSLEDEK = os.path.join(os.path.dirname(FRONTA), "vysledek.md")
MAX_ZNAKU = int(os.environ.get("MAX_ZNAKU", "20000"))      # pojistka: víc znaků v jednom běhu nenamluví
CFG = json.load(open(os.path.join(HERE, "hlasy.json"), encoding="utf-8"))

class Chyba(Exception): pass

def cesta(rel, pripona=None):
    p = os.path.realpath(os.path.join(REPO, rel))
    if not p.startswith(os.path.realpath(os.path.join(REPO, "Naučná videa")) + os.sep): raise Chyba(f"cesta mimo „Naučná videa/“: {rel}")
    if pripona and not p.endswith(pripona): raise Chyba(f"{rel} nekončí na {pripona}")
    return p

def text_ulohy(u):
    s = open(cesta(u["text"]), encoding="utf-8").read()
    if u.get("sekce"):
        m = re.search(r"^## " + re.escape(str(u["sekce"])) + r"\b[^\n]*\n.*?^```[^\n]*\n(.*?)^```", s, re.S | re.M)
        if not m: raise Chyba(f"v {u['text']} chybí sekce „## {u['sekce']}“ s blokem ```")
        s = m.group(1)
    s = s.strip()
    if not s: raise Chyba("prázdný text")
    return s

def api(method, path, data=None):
    req = urllib.request.Request(f"{API}{path}", method=method, data=None if data is None else json.dumps(data).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        raise Chyba(f"HTTP {e.code}: {' '.join(e.read().decode('utf-8', 'replace').split())[:300]}")

def namluv(u, text):
    j = CFG["jazyky"][u["jazyk"]]
    body = {"text": text, "model_id": u.get("model_id", CFG["model_id"]),
            "voice_settings": dict(CFG["voice_settings"], **u.get("voice_settings", {}))}
    if j.get("language_code"): body["language_code"] = j["language_code"]
    r = api("POST", f"/v1/text-to-speech/{j['voice_id']}/with-timestamps?output_format={CFG['output_format']}", body)
    audio = base64.b64decode(r["audio_base64"])
    out = cesta(u["vystup"], ".mp3"); os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "wb").write(audio)
    casy = {"text": text, "jazyk": u["jazyk"], "hlas": j["hlas"], "voice_id": j["voice_id"], "model_id": body["model_id"],
            "voice_settings": body["voice_settings"], "namluveno": datetime.date.today().isoformat(),
            "alignment": r.get("alignment"), "normalized_alignment": r.get("normalized_alignment")}
    with open(out[:-4] + ".casy.json", "w", encoding="utf-8") as f: json.dump(casy, f, ensure_ascii=False)
    return len(audio)

def main():
    fronta = json.load(open(FRONTA, encoding="utf-8")); ulohy = fronta.get("ulohy", [])
    if not ulohy: print("Fronta je prázdná."); return 0
    plan, vysl, zbyva = [], [], []
    for u in ulohy:
        popis = f"{u.get('jazyk', '?')} → {u.get('vystup', '?')}"
        try:
            if u.get("jazyk") not in CFG["jazyky"]: raise Chyba(f"jazyk {u.get('jazyk')} chybí v hlasy.json")
            if not CFG["jazyky"][u["jazyk"]].get("voice_id"): raise Chyba(f"hlas pro {u['jazyk']} nemá v hlasy.json voice_id")
            out = cesta(u.get("vystup", ""), ".mp3")
            if os.path.exists(out) and not u.get("znovu"): vysl.append((popis, "⏭ už existuje – přeskočeno (\"znovu\": true namluví znovu)")); continue
            plan.append((u, popis, text_ulohy(u)))
        except (Chyba, OSError, KeyError) as ex:
            vysl.append((popis, f"❌ {ex}")); zbyva.append(u)
    znaku = sum(len(t) for _, _, t in plan)
    print(f"K namluvení: {len(plan)} úloh, {znaku} znaků (limit běhu {MAX_ZNAKU})")
    if plan and znaku > MAX_ZNAKU:
        vysl += [(p, f"❌ dávka má {znaku} znaků, víc než limit {MAX_ZNAKU} – rozdělte ji") for _, p, _ in plan]; zbyva += [u for u, _, _ in plan]; plan = []
    if plan and not os.environ.get("ELEVENLABS_API_KEY"):
        vysl += [(p, "❌ chybí tajemství ELEVENLABS_API_KEY (Settings → Secrets and variables → Actions)") for _, p, _ in plan]
        zbyva += [u for u, _, _ in plan]; plan = []
    for u, popis, text in plan:
        try:
            b = namluv(u, text); vysl.append((popis, f"✅ {len(text)} znaků, {b / 1e3:.0f} kB")); print(f"✅ {popis}")
        except (Chyba, OSError, KeyError, ValueError) as ex:
            vysl.append((popis, f"❌ {ex}")); zbyva.append(u); print(f"❌ {popis}: {ex}")
    kredity = ""
    if os.environ.get("ELEVENLABS_API_KEY") and plan:
        try:
            s = api("GET", "/v1/user/subscription")
            kredity = f"\nZbývá kreditů: {s['character_limit'] - s['character_count']} z {s['character_limit']}\n"
        except (Chyba, KeyError): pass        # klíč bez práva číst účet – nevadí
    fronta["ulohy"] = zbyva
    with open(FRONTA, "w", encoding="utf-8") as f: f.write(json.dumps(fronta, ensure_ascii=False, indent=2) + "\n")
    cas = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with open(VYSLEDEK, "w", encoding="utf-8") as f:
        f.write(f"# Poslední běh „Namluvit“ – {cas}\n\n| Úloha | Výsledek |\n|---|---|\n")
        f.writelines(f"| {p} | {r.replace('|', '/')} |\n" for p, r in vysl)
        f.write(kredity)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f: f.write(open(VYSLEDEK, encoding="utf-8").read())
    print(open(VYSLEDEK, encoding="utf-8").read())
    return 1 if zbyva else 0

if __name__ == "__main__":
    sys.exit(main())
