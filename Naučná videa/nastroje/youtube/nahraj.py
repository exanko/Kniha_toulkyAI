"""Nahrání jazykových verzí dílu na YouTube podle souboru <díl>/youtube.json.

  python3 nahraj.py 09                 → nahraje všechny jazyky dílu 09, které ještě nemají videoId
  python3 nahraj.py 09 es hi           → jen vybrané jazyky
  python3 nahraj.py 09 --zkouska       → nic nenahraje: zkontroluje údaje a soubory, a jsou-li zadané
                                         přihlašovací údaje, ověří přihlášení, kanál a playlisty
  python3 nahraj.py 09 es --verejne    → zveřejní hned (jinak se nahrává jako soukromé)
  python3 nahraj.py 09 es --znovu      → nahraje znovu i jazyk, který už videoId má

Přihlašovací údaje v proměnných prostředí (v GitHub Actions z tajemství):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
Po každém úspěšném nahrání se videoId hned zapíše do youtube.json – opakované spuštění
tak video nenahraje dvakrát. Nakonec se playlisty zvolených jazyků seřadí podle čísel dílů
(jen ty, v nichž jsou pouze videa evidovaná v repu) – i když se nic nenahrávalo, takže
`python3 nahraj.py 09 es` u už nahraného dílu jen srovná španělský playlist.
Jen standardní knihovna Pythonu (bez instalace balíčků)."""
import glob, json, os, sys, time, datetime, urllib.request, urllib.parse, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("NAUCNA_VIDEA") or os.path.dirname(os.path.dirname(HERE))   # složka „Naučná videa“
API = os.environ.get("YT_API_BASE", "https://www.googleapis.com")
TOKEN_URL = os.environ.get("YT_TOKEN_URL", "https://oauth2.googleapis.com/token")
CFG = json.load(open(os.path.join(HERE, "kanal.json"), encoding="utf-8"))   # playlisty a kódy jazyků

def najdi_dil(arg):
    p = os.path.join(ROOT, arg)
    if os.path.isdir(p): return p
    m = sorted(glob.glob(os.path.join(ROOT, f"{arg}-*")))
    if len(m) != 1: sys.exit(f"Díl „{arg}“ nenalezen (nebo nejednoznačný): {m}")
    return m[0]

class HttpChyba(RuntimeError):
    def __init__(self, code, msg): super().__init__(msg); self.code = code

def http(method, url, token=None, data=None, headers=None, raw=False):
    h = dict(headers or {})
    if token: h["Authorization"] = f"Bearer {token}"
    if data is not None and not isinstance(data, (bytes, bytearray)):
        data = json.dumps(data).encode("utf-8"); h.setdefault("Content-Type", "application/json; charset=UTF-8")
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            body = r.read()
            return (r, body) if raw else json.loads(body or b"{}")
    except urllib.error.HTTPError as e:
        raise HttpChyba(e.code, f"{method} {url.split('?')[0]} → HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:800]}")

def access_token():
    miss = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(k)]
    if miss: sys.exit("Chybí přihlašovací údaje: " + ", ".join(miss) + " (v GitHubu: Settings → Secrets and variables → Actions)")
    form = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                   "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    r = http("POST", TOKEN_URL, data=form, headers={"Content-Type": "application/x-www-form-urlencoded"})
    return r["access_token"]

def zkontroluj(L, e, dil):
    chyby = []
    if not os.path.exists(os.path.join(dil, e.get("soubor", ""))): chyby.append(f"soubor {e.get('soubor')} neexistuje")
    n, p = e.get("nazev", ""), e.get("popis", "")
    if not n or len(n) > 100: chyby.append(f"název má {len(n)} znaků (1–100)")
    if len(p.encode("utf-8")) > 5000: chyby.append("popis je delší než 5000 bajtů")
    if any(c in n + p for c in "<>"): chyby.append("název ani popis nesmí obsahovat < nebo >")
    if len(",".join(e.get("stitky", []))) > 450: chyby.append("štítky jsou dohromady delší než ~450 znaků")
    if L not in CFG["jazyky"]: chyby.append(f"jazyk {L} chybí v kanal.json")
    return chyby

def over_pristup():
    """Zkouška bez nahrávání: přihlášení, kanál a existence playlistů (stojí 2 jednotky kvóty)."""
    token = access_token()
    ch = http("GET", f"{API}/youtube/v3/channels?part=snippet&mine=true", token).get("items", [])
    if not ch: sys.exit("❌ Přihlášení funguje, ale účet nemá kanál YouTube (u značkového účtu vyberte při přihlášení kanál).")
    print(f"🔑 Přihlášení OK – kanál „{ch[0]['snippet']['title']}“ ({ch[0]['id']})")
    pls = {L: v["playlist"] for L, v in CFG["jazyky"].items() if v.get("playlist")}
    q = urllib.parse.quote(",".join(pls.values()))
    found = {i["id"]: i["snippet"]["title"] for i in http("GET", f"{API}/youtube/v3/playlists?part=snippet&maxResults=50&id={q}", token).get("items", [])}
    ok = True
    for L, pid in pls.items():
        if pid in found: print(f"   📃 {L}: playlist „{found[pid]}“")
        else: print(f"   ❌ {L}: playlist {pid} nenalezen – opravte ho v kanal.json"); ok = False
    if not ok: sys.exit(1)
    return token

def nahraj(token, L, e, dil, verejne, spol):
    lang = CFG["jazyky"][L]["kod"]
    meta = {"snippet": {"title": e["nazev"], "description": e["popis"], "tags": e.get("stitky", []),
                        "categoryId": spol.get("categoryId", "27"), "defaultLanguage": lang, "defaultAudioLanguage": lang},
            "status": {"privacyStatus": "public" if verejne else "private", "embeddable": True,
                       "selfDeclaredMadeForKids": spol.get("madeForKids", False),
                       "containsSyntheticMedia": spol.get("containsSyntheticMedia", False)}}
    path = os.path.join(dil, e["soubor"]); size = os.path.getsize(path)
    r, _ = http("POST", f"{API}/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status", token, meta,
                {"X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)}, raw=True)
    loc = r.headers["Location"]; data = open(path, "rb").read()
    for pokus in range(1, 4):
        try:
            res = http("PUT", loc, token, data, {"Content-Type": "video/mp4", "Content-Length": str(size)})
            break
        except (HttpChyba, OSError) as ex:
            if pokus == 3 or (isinstance(ex, HttpChyba) and ex.code < 500): raise
            print(f"   pokus {pokus} selhal ({ex}), zkouším znovu…"); time.sleep(5 * pokus)
    return res["id"]

def pozice(token, L, dil, pl):
    """Pořadí v playlistu podle čísla dílu – jen když playlist obsahuje právě videa evidovaná
    v youtube.json (jinak, např. u ručně nahraných CZ/EN, se video přidá na konec)."""
    try: cislo = int(os.path.basename(dil)[:2])
    except ValueError: return None
    evid = []
    for f in glob.glob(os.path.join(ROOT, "*", "youtube.json")):
        if os.path.dirname(f) == dil: continue
        e = json.load(open(f, encoding="utf-8")).get("jazyky", {}).get(L, {})
        if e.get("videoId"):
            try: evid.append(int(os.path.basename(os.path.dirname(f))[:2]))
            except ValueError: return None
    r = http("GET", f"{API}/youtube/v3/playlistItems?part=id&maxResults=1&playlistId={urllib.parse.quote(pl)}", token)
    if r.get("pageInfo", {}).get("totalResults") != len(evid): return None
    return sum(1 for c in evid if c < cislo)

def do_playlistu(token, vid, pl, pos=None):
    """Zařadí video do playlistu; vrátí skutečnou pozici (None = na konec).
    Pozici YouTube přijme jen u playlistu s ručním řazením – jinak se video přidá na konec."""
    sn = {"playlistId": pl, "resourceId": {"kind": "youtube#video", "videoId": vid}}
    if pos is not None:
        try:
            http("POST", f"{API}/youtube/v3/playlistItems?part=snippet", token, {"snippet": dict(sn, position=pos)})
            return pos
        except HttpChyba as ex:
            if ex.code != 400 or "manualSortRequired" not in str(ex): raise
            print("   playlist nemá ruční řazení – přidávám na konec")
    http("POST", f"{API}/youtube/v3/playlistItems?part=snippet", token, {"snippet": sn})
    return None

def polozky(token, pl):
    """Položky playlistu v pořadí: [(id položky, videoId)] (1 jednotka kvóty za 50 položek)."""
    out, page = [], ""
    while True:
        r = http("GET", f"{API}/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={urllib.parse.quote(pl)}"
                        + (f"&pageToken={urllib.parse.quote(page)}" if page else ""), token)
        out += [(i["id"], i["snippet"]["resourceId"]["videoId"]) for i in r.get("items", [])]
        page = r.get("nextPageToken")
        if not page: return out

def evidovana(L):
    """videoId → číslo dílu pro všechna videa jazyka L zapsaná v youtube.json."""
    m = {}
    for f in glob.glob(os.path.join(ROOT, "*", "youtube.json")):
        vid = json.load(open(f, encoding="utf-8")).get("jazyky", {}).get(L, {}).get("videoId")
        if vid:
            try: m[vid] = int(os.path.basename(os.path.dirname(f))[:2])
            except ValueError: pass
    return m

def srovnej(token, L, pl, jen_zjistit=False, cekej_na=()):
    """Seřadí playlist jazyka L podle čísel dílů – jen když v něm jsou pouze videa evidovaná v repu.
    S ručním řazením položky přesune; bez něj přidá videa, která nejsou na svém místě, znovu na konec
    ve správném pořadí a starou položku smaže až potom (video tak z playlistu nikdy nevypadne).
    Funguje, dokud je v nastavení playlistu vypnuté „Přidávat nová videa na začátek“."""
    ev = evidovana(L)
    for pokus in range(4):                      # čerstvě přidané video se v seznamu objeví se zpožděním
        items = polozky(token, pl); vids = [v for _, v in items]
        if all(v in vids for v in cekej_na): break
        if pokus == 3: return "nové video se v playlistu zatím neukázalo – pořadí srovná příští spuštění"
        time.sleep(5)
    if any(v not in ev for v in vids) or len(set(vids)) != len(vids):
        return "pořadí neřeším – v playlistu jsou i videa, která repo nezná"
    chtene = sorted(vids, key=lambda v: ev[v])
    if vids == chtene: return "pořadí v pořádku"
    if jen_zjistit: return "pořadí nesedí – srovná se při spuštění bez zkoušky"
    res = lambda v: {"kind": "youtube#video", "videoId": v}
    cur, n = list(items), 0
    try:
        for i, v in enumerate(chtene):
            if cur[i][1] == v: continue
            j = next(k for k in range(i, len(cur)) if cur[k][1] == v)
            http("PUT", f"{API}/youtube/v3/playlistItems?part=snippet", token,
                 {"id": cur[j][0], "snippet": {"playlistId": pl, "resourceId": res(v), "position": i}})
            cur.insert(i, cur.pop(j)); n += 1
        return f"pořadí srovnáno (přesunuto {n})"
    except HttpChyba as ex:
        if n or ex.code != 400 or "manualSortRequired" not in str(ex): raise
    poz = {v: k for k, v in enumerate(vids)}; k, posl = 0, -1
    while k < len(chtene) and poz[chtene[k]] > posl: posl = poz[chtene[k]]; k += 1   # začátek, který už sedí
    for v in chtene[k:]:
        stara = next(i for i, w in items if w == v)
        http("POST", f"{API}/youtube/v3/playlistItems?part=snippet", token, {"snippet": {"playlistId": pl, "resourceId": res(v)}})
        http("DELETE", f"{API}/youtube/v3/playlistItems?id={urllib.parse.quote(stara)}", token)
    for pokus in range(4):                      # seznam se po změnách obnovuje se zpožděním
        time.sleep(5)
        if [v for _, v in polozky(token, pl)] == chtene: return f"pořadí srovnáno (znovu přidáno {len(chtene) - k})"
    return "pořadí se nepodařilo ověřit – zkontrolujte playlist (vypnuté „Přidávat nová videa na začátek“?)"

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]; flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args: sys.exit(__doc__)
    dil = najdi_dil(args[0]); jpath = os.path.join(dil, "youtube.json")
    cfg = json.load(open(jpath, encoding="utf-8")); spol = cfg.get("spolecne", {})
    langs = args[1:] or list(cfg["jazyky"])
    zkouska, verejne, znovu = "--zkouska" in flags, "--verejne" in flags, "--znovu" in flags
    plan, chyby = [], []
    for L in langs:
        e = cfg["jazyky"].get(L)
        if not e: chyby.append(f"{L}: v youtube.json chybí"); continue
        if e.get("videoId") and not znovu: print(f"⏭  {L}: už nahráno ({e['videoId']}) – přeskakuji"); continue
        ch = zkontroluj(L, e, dil)
        if ch: chyby += [f"{L}: {c}" for c in ch]
        else: plan.append(L)
    if chyby: print("❌ Chyby v údajích:\n  " + "\n  ".join(chyby)); sys.exit(1)
    print(f"Díl {os.path.basename(dil)} – k nahrání: {', '.join(plan) or 'nic'}"
          f" ({'veřejně' if verejne else 'soukromě'}{', ZKOUŠKA' if zkouska else ''})")
    for L in plan:
        e = cfg["jazyky"][L]
        print(f"   {L}: {e['soubor']} ({os.path.getsize(os.path.join(dil, e['soubor'])) / 1e6:.1f} MB) · „{e['nazev']}“"
              f" · playlist {CFG['jazyky'][L].get('playlist') or '–'}")
    creds = all(os.environ.get(k) for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"))
    if zkouska:
        if not creds: print("(přihlašovací údaje nejsou zadané – přihlášení a playlisty se neověřují)"); return
        token = over_pristup()
        for L in langs:
            pl = CFG["jazyky"].get(L, {}).get("playlist")
            if pl: print(f"   📃 {L}: {srovnej(token, L, pl, jen_zjistit=True)}")
        return
    if not plan and not creds: return
    token = access_token(); souhrn, nove = [], {}
    for L in plan:
        e = cfg["jazyky"][L]
        vid = nahraj(token, L, e, dil, verejne, spol)
        e["videoId"] = vid; e["url"] = f"https://www.youtube.com/shorts/{vid}"
        e["nahrano"] = datetime.date.today().isoformat()
        with open(jpath, "w", encoding="utf-8") as f: f.write(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")
        pl = CFG["jazyky"][L].get("playlist"); stav = "nahráno"
        if pl:
            try:
                pos = do_playlistu(token, vid, pl, pozice(token, L, dil, pl)); nove[L] = vid
                stav += ", v playlistu" + (f" (pozice {pos + 1})" if pos is not None else " (na konci)")
            except HttpChyba as ex:
                stav += f", playlist SELHAL – přidejte ho ručně (HTTP {ex.code})"; print("   " + str(ex))
        print(f"✅ {L}: {e['url']} ({stav})"); souhrn.append((L, e["url"], stav))
    for L in langs:                              # pořadí v playlistech podle čísel dílů
        pl = CFG["jazyky"].get(L, {}).get("playlist")
        if not pl: continue
        try: stav = srovnej(token, L, pl, cekej_na=[nove[L]] if L in nove else [])
        except HttpChyba as ex: stav = f"řazení SELHALO (HTTP {ex.code}) – srovnejte playlist ručně"; print("   " + str(ex))
        print(f"📃 {L}: {stav}"); souhrn.append((L, "playlist", stav))
    if os.environ.get("GITHUB_STEP_SUMMARY") and souhrn:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(f"### {os.path.basename(dil)}\n\n| Jazyk | Video | Stav |\n|---|---|---|\n")
            f.writelines(f"| {L} | {u} | {' '.join(s.split()).replace('|', '/')[:200]} |\n" for L, u, s in souhrn)
            if plan and not verejne: f.write("\nVidea jsou **soukromá** – zveřejněte je v YouTube Studiu (a nastavte související video).\n")

if __name__ == "__main__":
    main()
