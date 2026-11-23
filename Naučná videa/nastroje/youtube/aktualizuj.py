"""Srovná už nahraná videa na YouTube s youtube.json: název, jazyk názvu a jazyk zvuku.
Popis a štítky doplní jen tam, kde na YouTube chybí (--prepsat-popis je přepíše podle youtube.json).

  python3 aktualizuj.py 01 02 cs en --zkouska   → jen vypíše, co by se změnilo (1 jednotka kvóty na 50 videí)
  python3 aktualizuj.py 01 02 cs en             → změny provede (50 jednotek za každé měněné video)
  python3 aktualizuj.py --vse --zkouska         → všechny díly a jazyky

Přihlašovací údaje YT_* jako u nahraj.py. Mění jen části snippet a localizations (stav, plánované
zveřejnění ani playlisty se nemění). Automaticky vytvořený překlad názvu ve starém jazyce videa
(např. „cs“ u anglického videa) nahradí překladem v novém jazyce; jiné překlady nechá být."""
import glob, json, os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nahraj as N

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]; flags = {a for a in sys.argv[1:] if a.startswith("--")}
    zkouska, prepsat = "--zkouska" in flags, "--prepsat-popis" in flags
    vyber = [a for a in args if a in N.CFG["jazyky"]]
    if "--vse" in flags: dily = sorted(os.path.dirname(f) for f in glob.glob(os.path.join(N.ROOT, "[0-9][0-9]-*", "youtube.json")))
    else: dily = [N.najdi_dil(a) for a in args if a not in N.CFG["jazyky"]]
    if not dily: sys.exit(__doc__)
    cile = []                                              # (díl, jazyk, záznam)
    for dil in dily:
        cfg = json.load(open(os.path.join(dil, "youtube.json"), encoding="utf-8"))
        for L, e in cfg["jazyky"].items():
            if (not vyber or L in vyber) and e.get("videoId"): cile.append((os.path.basename(dil)[:2], L, e))
    if not cile: print("Žádné nahrané video k porovnání."); return 0
    token = N.access_token()
    ted = {}
    ids = [e["videoId"] for _, _, e in cile]
    for i in range(0, len(ids), 50):
        q = urllib.parse.quote(",".join(ids[i:i + 50]))
        for v in N.api("GET", f"{N.API}/youtube/v3/videos?part=snippet,localizations&id={q}", token).get("items", []): ted[v["id"]] = v
    zmeneno, chyby = 0, 0
    for d, L, e in cile:
        v = ted.get(e["videoId"])
        if not v: print(f"❌ {d} {L}: video {e['videoId']} na YouTube není"); chyby += 1; continue
        s, kod = v["snippet"], N.CFG["jazyky"][L]["kod"]
        novy = {"title": e["nazev"], "categoryId": s.get("categoryId", "27"), "defaultLanguage": kod, "defaultAudioLanguage": kod,
                "description": e["popis"] if prepsat or not s.get("description", "").strip() else s["description"],
                "tags": e.get("stitky", []) if prepsat or not s.get("tags") else s["tags"]}
        lok = dict(v.get("localizations", {}))
        stary = s.get("defaultLanguage")
        if stary and stary != kod and lok.get(stary, {}).get("title") == s.get("title"): lok.pop(stary)   # automatický překlad starého jazyka
        lok[kod] = {"title": novy["title"], "description": novy["description"]}
        zmeny = []
        if s.get("title") != novy["title"]: zmeny.append(f"název „{s.get('title')}“ → „{novy['title']}“")
        if stary != kod: zmeny.append(f"jazyk názvu {stary or '–'} → {kod}")
        if s.get("defaultAudioLanguage") != kod: zmeny.append(f"jazyk zvuku {s.get('defaultAudioLanguage') or '–'} → {kod}")
        if s.get("description", "") != novy["description"]: zmeny.append("popis " + ("doplněn" if not s.get("description", "").strip() else "přepsán"))
        if (s.get("tags") or []) != novy["tags"]: zmeny.append("štítky " + ("doplněny" if not s.get("tags") else "přepsány"))
        if v.get("localizations", {}) != lok and not zmeny: zmeny.append("překlady názvu")
        if not zmeny: print(f"   {d} {L}: beze změny"); continue
        print(f"{'🔎' if zkouska else '✏️ '} {d} {L} ({e['videoId']}): " + "; ".join(zmeny))
        if zkouska: continue
        try:
            N.api("PUT", f"{N.API}/youtube/v3/videos?part=snippet,localizations", token,
                  {"id": e["videoId"], "snippet": novy, "localizations": lok})
            zmeneno += 1
        except (N.HttpChyba, N.Kvota) as ex:
            print(f"❌ {d} {L}: {ex}"); chyby += 1
    print(f"\n{'Zkouška – nic nezměněno' if zkouska else f'Změněno {zmeneno} videí'}; chyb {chyby}; spotřeba kvóty ≈ {N.STAV['jednotky']} jednotek")
    return 1 if chyby else 0

if __name__ == "__main__":
    sys.exit(main())
