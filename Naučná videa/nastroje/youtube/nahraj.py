"""Nahrání jazykových verzí dílů na YouTube podle <díl>/youtube.json a údržba playlistů.

  python3 nahraj.py 09                 → nahraje všechny jazyky dílu 09, které ještě nemají videoId
  python3 nahraj.py 09 10 es hi        → víc dílů, jen vybrané jazyky
  python3 nahraj.py --vse              → všechny díly (workflow po sloučení do main a jednou denně)
  python3 nahraj.py 09 --zkouska       → nic nenahraje ani nezmění: zkontroluje údaje a soubory, a jsou-li
                                         zadané přihlašovací údaje, ověří přihlášení a vypíše obsah playlistů
  python3 nahraj.py 09 es --verejne    → zveřejní hned (jinak se nahrává jako soukromé)
  python3 nahraj.py 09 --naplanovat    → naplánuje zveřejnění: v každém jazyce jedno video denně,
                                         v čase a pásmu z kanal.json („zverejneni“), od zítřka nebo
                                         den po posledním naplánovaném; předem zapsané „zverejneni“
                                         v youtube.json (např. "2026-12-01T18:00") má přednost
  python3 nahraj.py 09 es --znovu      → nahraje znovu i jazyk, který už videoId má

Přihlašovací údaje v proměnných prostředí (v GitHub Actions z tajemství):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN

Po každém úspěšném nahrání se videoId hned zapíše do youtube.json – opakované spuštění tak video
nenahraje dvakrát. Playlisty dotčených jazyků (u --vse všech) se udržují jednou za běh:
  1. odstraní se zdvojené položky evidovaných videí a doplní chybějící evidovaná videa,
  2. po nahrání se playlist s ručním řazením seřadí podle čísel dílů (jen když obsahuje výhradně
     evidovaná videa). Playlist s automatickým řazením (podle data) seřadit nejde – jen se ohlásí.
Skript nikdy nedělá dvojici „přidat znovu + smazat“: každý krok je samostatně bezpečný, takže
přerušený běh nenechá playlist rozbitý. Při vyčerpání kvóty (HTTP 403 quotaExceeded) počká minutu,
zkusí to ještě jednou a pak další volání vynechá – zbytek dodělá příští běh (workflow běží i denně).
Návratový kód 1 = něco zbylo nebo selhalo (běh workflow zčervená), 0 = vše hotovo.
Jen standardní knihovna Pythonu (bez instalace balíčků)."""
import glob, json, os, sys, time, datetime, urllib.request, urllib.parse, urllib.error
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("NAUCNA_VIDEA") or os.path.dirname(os.path.dirname(HERE))   # složka „Naučná videa“
API = os.environ.get("YT_API_BASE", "https://www.googleapis.com")
TOKEN_URL = os.environ.get("YT_TOKEN_URL", "https://oauth2.googleapis.com/token")
CFG = json.load(open(os.path.join(HERE, "kanal.json"), encoding="utf-8"))   # playlisty a kódy jazyků
CEKANI_KVOTA = float(os.environ.get("YT_CEKANI_KVOTA", "60"))     # pauza před druhým pokusem po quotaExceeded
CEKANI_SEZNAM = float(os.environ.get("YT_CEKANI_SEZNAM", "10"))   # pauza mezi dvěma výpisy playlistu
CENA = {"GET": 1, "POST": 50, "PUT": 50, "DELETE": 50}            # jednotky kvóty (playlistItems)
KVOTA = {"quotaExceeded", "dailyLimitExceeded", "rateLimitExceeded", "userRateLimitExceeded", "uploadLimitExceeded"}
STAV = {"kvota": False, "kvota_nahrani": False, "jednotky": 0}   # nahrávání videí má vlastní denní limit
PROBLEMY = []                                                     # co zbylo / selhalo → návratový kód 1

def najdi_dil(arg):
    p = os.path.join(ROOT, arg)
    if os.path.isdir(p): return p
    m = sorted(glob.glob(os.path.join(ROOT, f"{arg}-*")))
    if len(m) != 1: sys.exit(f"Díl „{arg}“ nenalezen (nebo nejednoznačný): {m}")
    return m[0]

def cislo_dilu(path):
    try: return int(os.path.basename(path)[:2])
    except ValueError: return None

class HttpChyba(RuntimeError):
    def __init__(self, code, msg, reason=""): super().__init__(msg); self.code = code; self.reason = reason

class Kvota(RuntimeError):
    pass

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
        body = e.read().decode("utf-8", "replace"); reason = ""
        try: reason = json.loads(body)["error"]["errors"][0].get("reason", "")
        except (ValueError, KeyError, IndexError, TypeError): pass
        raise HttpChyba(e.code, f"{method} {url.split('?')[0]} → HTTP {e.code} {reason}: {body[:300]}", reason)

def api(method, url, token, data=None, raw=False, headers=None):
    """Volání YouTube API s ohledem na kvótu: po quotaExceeded jednou počká a zkusí znovu,
    pak nastaví příznak kvóty a další volání stejného druhu v tomto běhu rovnou vynechá (Kvota).
    Nahrávání videí (/upload/) má od YouTube vlastní denní limit, proto vlastní příznak."""
    klic = "kvota_nahrani" if "/upload/" in url else "kvota"
    cena = 0 if "/upload/" in url else CENA.get(method, 0)
    if STAV[klic]: raise Kvota("kvóta je vyčerpaná – vynecháno")
    for pokus in (1, 2):
        try:
            r = http(method, url, token, data, headers, raw)
            STAV["jednotky"] += cena; return r
        except HttpChyba as ex:
            STAV["jednotky"] += cena                         # i odmítnutý požadavek kvótu stojí
            if ex.code == 403 and ex.reason in KVOTA:
                if pokus == 1:
                    print(f"   ⏳ kvóta ({ex.reason}) – čekám {CEKANI_KVOTA:.0f} s a zkusím to znovu"); time.sleep(CEKANI_KVOTA); continue
                STAV[klic] = True; raise Kvota(str(ex))
            raise

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

def over_pristup(token):
    """Zkouška: přihlášení, kanál a existence playlistů (2 jednotky kvóty)."""
    ch = api("GET", f"{API}/youtube/v3/channels?part=snippet&mine=true", token).get("items", [])
    if not ch: sys.exit("❌ Přihlášení funguje, ale účet nemá kanál YouTube (u značkového účtu vyberte při přihlášení kanál).")
    print(f"🔑 Přihlášení OK – kanál „{ch[0]['snippet']['title']}“ ({ch[0]['id']})")
    pls = {L: v["playlist"] for L, v in CFG["jazyky"].items() if v.get("playlist")}
    q = urllib.parse.quote(",".join(pls.values()))
    found = {i["id"]: i["snippet"]["title"] for i in api("GET", f"{API}/youtube/v3/playlists?part=snippet&maxResults=50&id={q}", token).get("items", [])}
    for L, pid in pls.items():
        if pid in found: print(f"   📃 {L}: playlist „{found[pid]}“")
        else: print(f"   ❌ {L}: playlist {pid} nenalezen – opravte ho v kanal.json"); PROBLEMY.append(f"{L}: playlist nenalezen")

def termin(L, e, po=None):
    """Plánované zveřejnění jazyka L: předem zapsané e["zverejneni"], jinak další volný den
    (po = termín, který už je v tomto výpisu obsazený – jen pro zkoušku a přehled)."""
    z = CFG["jazyky"][L].get("zverejneni", {"cas": "18:00", "zona": "Europe/Prague"}); tz = ZoneInfo(z["zona"])
    h, m = map(int, z["cas"].split(":"))
    if e.get("zverejneni"):
        t = datetime.datetime.fromisoformat(e["zverejneni"])
        return t if t.tzinfo else t.replace(tzinfo=tz)
    ted = datetime.datetime.now(tz); den = ted.date() + datetime.timedelta(days=1)
    for f in glob.glob(os.path.join(ROOT, "*", "youtube.json")):
        x = json.load(open(f, encoding="utf-8")).get("jazyky", {}).get(L, {})
        if x.get("videoId") and x.get("zverejneni"):
            t = datetime.datetime.fromisoformat(x["zverejneni"])
            t = (t if t.tzinfo else t.replace(tzinfo=tz)).astimezone(tz)
            den = max(den, t.date() + datetime.timedelta(days=1))
    if po: den = max(den, po.astimezone(tz).date() + datetime.timedelta(days=1))
    return datetime.datetime(den.year, den.month, den.day, h, m, tzinfo=tz)

def nahraj(token, L, e, dil, verejne, spol, kdy=None):
    lang = CFG["jazyky"][L]["kod"]
    stat = {"privacyStatus": "public" if verejne and not kdy else "private"}
    if kdy: stat["publishAt"] = kdy.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    meta = {"snippet": {"title": e["nazev"], "description": e["popis"], "tags": e.get("stitky", []),
                        "categoryId": spol.get("categoryId", "27"), "defaultLanguage": lang, "defaultAudioLanguage": lang},
            "status": {**stat, "embeddable": True,
                       "selfDeclaredMadeForKids": spol.get("madeForKids", False),
                       "containsSyntheticMedia": spol.get("containsSyntheticMedia", False)}}
    path = os.path.join(dil, e["soubor"]); size = os.path.getsize(path)
    r, _ = api("POST", f"{API}/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status", token, meta, raw=True,
               headers={"X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    loc = r.headers["Location"]; data = open(path, "rb").read()
    for pokus in range(1, 4):
        try:
            res = http("PUT", loc, token, data, {"Content-Type": "video/mp4", "Content-Length": str(size)})
            break
        except (HttpChyba, OSError) as ex:
            if pokus == 3 or (isinstance(ex, HttpChyba) and ex.code < 500): raise
            print(f"   pokus {pokus} selhal ({ex}), zkouším znovu…"); time.sleep(5 * pokus)
    return res["id"]

# ---------- playlisty ----------

def evidovana(L):
    """videoId → číslo dílu pro všechna videa jazyka L zapsaná v youtube.json."""
    m = {}
    for f in glob.glob(os.path.join(ROOT, "*", "youtube.json")):
        vid = json.load(open(f, encoding="utf-8")).get("jazyky", {}).get(L, {}).get("videoId")
        c = cislo_dilu(os.path.dirname(f))
        if vid and c is not None: m[vid] = c
    return m

def zaznamy(L):
    """videoId → (cesta k youtube.json, playlist, do kterého už video bylo přidáno – nebo None)."""
    m = {}
    for f in glob.glob(os.path.join(ROOT, "*", "youtube.json")):
        e = json.load(open(f, encoding="utf-8")).get("jazyky", {}).get(L, {})
        if e.get("videoId"): m[e["videoId"]] = (f, e.get("playlist"))
    return m

def uloz(jpath, L, **pole):
    """Zapíše pole jednoho jazyka do youtube.json (soubor znovu načte – nic jiného nepřepíše); None = smazat pole."""
    cfg = json.load(open(jpath, encoding="utf-8")); e = cfg["jazyky"][L]
    for k, v in pole.items():
        if v is None: e.pop(k, None)
        else: e[k] = v
    with open(jpath, "w", encoding="utf-8") as f: f.write(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")

def polozky(token, pl):
    """Položky playlistu v pořadí: [(id položky, videoId)] (1 jednotka kvóty za 50 položek)."""
    out, page = [], ""
    while True:
        r = api("GET", f"{API}/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={urllib.parse.quote(pl)}"
                       + (f"&pageToken={urllib.parse.quote(page)}" if page else ""), token)
        out += [(i["id"], i["snippet"]["resourceId"]["videoId"]) for i in r.get("items", [])]
        page = r.get("nextPageToken")
        if not page: return out

class Playlist:
    """Stav playlistu během běhu. Načte se jednou (dva výpisy po sobě se musí shodovat – YouTube
    změny ukazuje se zpožděním) a dál se vede podle vlastních změn, ne podle dalších výpisů."""
    def __init__(self, token, L, pl):
        self.L, self.pl, self.rucni, self.ustaleny, self.neuplny = L, pl, None, False, False   # rucni: None = zatím nevíme
        self.items = polozky(token, pl)
        for _ in range(3):
            time.sleep(CEKANI_SEZNAM)
            znovu = polozky(token, pl)
            if znovu == self.items: self.ustaleny = True; break
            self.items = znovu

    def vids(self): return [v for _, v in self.items]

PLS = {}
def playlist(token, L):
    pl = CFG["jazyky"].get(L, {}).get("playlist")
    if not pl: return None
    if L not in PLS: PLS[L] = Playlist(token, L, pl)
    return PLS[L]

def popis(p, ev):
    """Obsah playlistu čísly dílů (? = video mimo repo). U automatického řazení určuje pořadí YouTube."""
    vids = p.vids()
    if p.rucni is False and all(v in ev for v in vids):
        return "obsah " + (" ".join(f"{c:02d}" for c in sorted(ev[v] for v in vids)) or "(prázdný)")
    return " ".join(f"{ev[v]:02d}" if v in ev else "?" for v in vids) or "(prázdný)"

def zarad(token, p, vid, ev):
    """Přidá video do playlistu (nanejvýš jednou). U playlistu s ručním řazením rovnou na místo podle
    čísla dílu, jinak na konec. Úspěch zapíše do youtube.json („playlist“), aby ho příští běh
    nepřidal znovu, ani kdyby ho výpis playlistu ještě neukazoval. Vrací popis pro výpis."""
    if vid in p.vids(): return "už v playlistu"
    r = pridej(token, p, vid, ev)
    zz = zaznamy(p.L).get(vid)
    if zz: uloz(zz[0], p.L, playlist=p.pl)
    return r

def pridej(token, p, vid, ev):
    sn = {"playlistId": p.pl, "resourceId": {"kind": "youtube#video", "videoId": vid}}
    if p.rucni is not False and vid in ev and all(v in ev for v in p.vids()):
        pos = 1 + max((k for k, v in enumerate(p.vids()) if ev[v] < ev[vid]), default=-1)   # za poslední nižší díl
        try:
            r = api("POST", f"{API}/youtube/v3/playlistItems?part=snippet", token, {"snippet": dict(sn, position=pos)})
            p.rucni = True; p.items.insert(pos, (r.get("id", f"?{vid}"), vid)); return f"v playlistu (pozice {pos + 1})"
        except HttpChyba as ex:
            if ex.code != 400 or ex.reason != "manualSortRequired": raise
            p.rucni = False
    r = api("POST", f"{API}/youtube/v3/playlistItems?part=snippet", token, {"snippet": sn})
    p.items.append((r.get("id", f"?{vid}"), vid)); return "v playlistu (na konci)"

def oprav(token, L):
    """Krok 1 údržby: smaže zdvojené položky evidovaných videí a doplní chybějící evidovaná videa."""
    p = playlist(token, L)
    if p is None: return
    ev = evidovana(L)
    print(f"📃 {L}: v playlistu {popis(p, ev)}")
    if not p.ustaleny:
        print(f"   {L}: výpis playlistu se ještě mění – opravy nechávám na příští běh"); PROBLEMY.append(f"{L}: playlist neustálený"); return
    videno, smazano = set(), []
    for iid, v in list(p.items):
        if v not in ev: continue
        if v in videno:
            try: api("DELETE", f"{API}/youtube/v3/playlistItems?id={urllib.parse.quote(iid)}", token)
            except HttpChyba as ex:
                if ex.code != 404: raise
            p.items.remove((iid, v)); smazano.append(f"{ev[v]:02d}")
        else: videno.add(v)
    if smazano: print(f"   {L}: smazána zdvojená položka – díl {', '.join(smazano)}")
    zz = zaznamy(L)
    for v in set(p.vids()):                         # u videí, která v playlistu jsou, zapsat, že tam patří
        if v in zz and zz[v][1] != p.pl: uloz(zz[v][0], L, playlist=p.pl)
    chybi = [v for v in sorted(ev, key=ev.get) if v not in p.vids()]
    uz = [v for v in chybi if zz.get(v, (None, None))[1] == p.pl]   # už přidané – znovu ne (hrozilo by zdvojení)
    p.neuplny = bool(uz)
    if uz: print(f"   {L}: ve výpisu zatím není díl {' '.join(f'{ev[v]:02d}' for v in uz)} – do playlistu už přidaný byl"
                 " (ještě se neukázal, nebo byl ručně odebrán), znovu nepřidávám")
    for v in chybi:
        if v not in uz: print(f"   {L}: doplněn díl {ev[v]:02d} – {zarad(token, p, v, ev)}")

def serad(token, L):
    """Krok 2 údržby: playlist s ručním řazením seřadí podle čísel dílů; jinak jen ohlásí stav."""
    p = playlist(token, L)
    if p is None: return f"playlist není v kanal.json – přeskakuji"
    ev = evidovana(L); vids = p.vids()
    if not p.ustaleny: return "neověřeno (výpis playlistu se měnil)"
    zz = zaznamy(L)
    chybi = sorted(ev[v] for v in ev if v not in vids and zz.get(v, (None, None))[1] != p.pl)
    if chybi: return f"{popis(p, ev)} · chybí díl {' '.join(f'{c:02d}' for c in chybi)} – doplní příští běh"
    if any(v not in ev for v in vids): return f"{popis(p, ev)} · pořadí neřeším – v playlistu jsou i videa, která repo nezná"
    if p.neuplny: return f"{popis(p, ev)} · pořadí neřeším – výpis playlistu je zatím neúplný (ověří příští běh)"
    chtene = sorted(vids, key=lambda v: ev[v])
    if vids == chtene: return f"{popis(p, ev)} · pořadí v pořádku"
    if p.rucni is False: return f"{popis(p, ev)} · playlist má automatické řazení (podle data) – pořadí podle dílů jen při ručním řazení"
    n = 0
    for i, v in enumerate(chtene):
        if p.items[i][1] == v: continue
        j = next(k for k in range(i, len(p.items)) if p.items[k][1] == v)
        try:
            api("PUT", f"{API}/youtube/v3/playlistItems?part=snippet", token,
                {"id": p.items[j][0], "snippet": {"playlistId": p.pl, "resourceId": {"kind": "youtube#video", "videoId": v}, "position": i}})
        except HttpChyba as ex:
            if n == 0 and ex.code == 400 and ex.reason == "manualSortRequired":
                p.rucni = False
                return f"{popis(p, ev)} · playlist má automatické řazení (podle data) – pořadí podle dílů jen při ručním řazení"
            raise
        p.rucni = True; p.items.insert(i, p.items.pop(j)); n += 1
    return f"{popis(p, ev)} · pořadí srovnáno (přesunuto {n})"

def zjisti(token, L):
    """Zkouška: jen popíše stav playlistu (bez zápisu)."""
    pl = CFG["jazyky"].get(L, {}).get("playlist")
    if not pl: return "playlist není v kanal.json"
    ev = evidovana(L); items = polozky(token, pl); vids = [v for _, v in items]
    o = " ".join(f"{ev[v]:02d}" if v in ev else "?" for v in vids) or "(prázdný)"
    dvoj = sorted({ev[v] for v in vids if v in ev and vids.count(v) > 1})
    zz = zaznamy(L)
    chybi = sorted(ev[v] for v in ev if v not in vids and zz[v][1] != pl)
    uz = sorted(ev[v] for v in ev if v not in vids and zz[v][1] == pl)
    zprava = [o, f"{len(vids)} položek"]
    if dvoj: zprava.append("zdvojené: " + " ".join(f"{c:02d}" for c in dvoj))
    if chybi: zprava.append("chybí: " + " ".join(f"{c:02d}" for c in chybi))
    if uz: zprava.append("není ve výpisu, ale přidané už bylo: " + " ".join(f"{c:02d}" for c in uz))
    if any(v not in ev for v in vids): zprava.append("obsahuje i videa mimo repo")
    elif [v for v in vids] != sorted(vids, key=lambda v: ev[v]): zprava.append("pořadí nesedí")
    return " · ".join(zprava)

# ---------- hlavní běh ----------

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]; flags = {a for a in sys.argv[1:] if a.startswith("--")}
    zkouska, verejne, znovu, naplanovat, vse = (f in flags for f in ("--zkouska", "--verejne", "--znovu", "--naplanovat", "--vse"))
    vyber = [a for a in args if a in CFG["jazyky"]]
    if vse: dily = sorted(os.path.dirname(f) for f in glob.glob(os.path.join(ROOT, "[0-9][0-9]-*", "youtube.json")))
    else: dily = [najdi_dil(a) for a in args if a not in CFG["jazyky"]]
    if not dily: sys.exit(__doc__)
    plan, chyby, udrzovat = [], [], set()
    for dil in dily:
        jpath = os.path.join(dil, "youtube.json"); cfg = json.load(open(jpath, encoding="utf-8"))
        langs = vyber or list(cfg["jazyky"])
        if vse: langs = [L for L in langs if L in cfg["jazyky"]]     # u --vse díly bez zvoleného jazyka přeskočit
        udrzovat.update(langs)
        mam = []
        for L in langs:
            e = cfg["jazyky"].get(L)
            if not e: chyby.append(f"{os.path.basename(dil)} {L}: v youtube.json chybí"); continue
            if e.get("videoId") and not znovu: continue
            ch = zkontroluj(L, e, dil)
            if ch: chyby += [f"{os.path.basename(dil)} {L}: {c}" for c in ch]
            else: mam.append(L)
        if mam: plan.append((dil, jpath, cfg, mam))
    if vse and not vyber: udrzovat = set(CFG["jazyky"])
    udrzovat = [L for L in CFG["jazyky"] if L in udrzovat]
    if chyby: print("❌ Chyby v údajích:\n  " + "\n  ".join(chyby)); sys.exit(1)
    rezim = "naplánovaně" if naplanovat else "veřejně" if verejne else "soukromě"
    print(f"K nahrání ({rezim}{', ZKOUŠKA' if zkouska else ''}): " + (", ".join(f"{os.path.basename(d)[:2]} {' '.join(m)}" for d, _, _, m in plan) or "nic"))
    obsazeno = {}                                    # jazyk → poslední termín v tomto přehledu
    for dil, _, cfg, mam in plan:
        for L in mam:
            e = cfg["jazyky"][L]; kdy = ""
            if naplanovat:
                t = termin(L, e, obsazeno.get(L)); obsazeno[L] = t; kdy = f" · zveřejnění {t.isoformat(timespec='minutes')}"
            print(f"   {os.path.basename(dil)[:2]} {L}: {e['soubor']} ({os.path.getsize(os.path.join(dil, e['soubor'])) / 1e6:.1f} MB) · „{e['nazev']}“"
                  f" · playlist {CFG['jazyky'][L].get('playlist') or '–'}{kdy}")
    creds = all(os.environ.get(k) for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"))
    if zkouska:
        if not creds: print("(přihlašovací údaje nejsou zadané – přihlášení a playlisty se neověřují)"); return 0
        token = access_token(); over_pristup(token)
        for L in udrzovat:
            try: print(f"   📃 {L}: {zjisti(token, L)}")
            except (HttpChyba, Kvota) as ex: print(f"   📃 {L}: nelze zjistit – {ex}"); PROBLEMY.append(f"{L}: playlist nezjištěn")
        print(f"(spotřeba kvóty tohoto běhu ≈ {STAV['jednotky']} jednotek)")
        return 1 if PROBLEMY else 0
    if not creds:
        if plan: sys.exit("Chybí přihlašovací údaje YT_* – nic se nenahrálo.")
        return 0
    token = access_token(); souhrn = []

    for L in udrzovat:                               # 1) údržba: zdvojené a chybějící položky
        try: oprav(token, L)
        except Kvota: PROBLEMY.append(f"{L}: údržba playlistu nedokončena (kvóta)"); print(f"   {L}: kvóta vyčerpaná – údržbu dokončí příští běh")
        except HttpChyba as ex: PROBLEMY.append(f"{L}: údržba playlistu selhala"); print(f"   {L}: údržba playlistu selhala – {ex}")

    odlozit = set()                                  # jazyky, kde nahrání selhalo – další díly až příště (kvůli pořadí)
    for dil, jpath, cfg, mam in plan:                # 2) nahrání
        spol = cfg.get("spolecne", {})
        for L in mam:
            e = cfg["jazyky"][L]; d = os.path.basename(dil)[:2]
            if STAV["kvota_nahrani"]:
                PROBLEMY.append(f"{d} {L}: nenahráno (kvóta)"); souhrn.append((d, L, "–", "nenahráno – kvóta, nahraje příští běh")); continue
            if L in odlozit:
                PROBLEMY.append(f"{d} {L}: odloženo"); souhrn.append((d, L, "–", "odloženo – nejdřív se musí nahrát dřívější díl (pořadí zveřejnění)")); continue
            kdy = termin(L, e) if naplanovat else None
            if kdy and kdy <= datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30):
                print(f"   {d} {L}: termín {kdy.isoformat()} už je pryč – plánuji na další volný den"); e.pop("zverejneni", None); kdy = termin(L, e)
            try: vid = nahraj(token, L, e, dil, verejne, spol, kdy)
            except (HttpChyba, Kvota, OSError) as ex:
                print(f"❌ {d} {L}: nahrání selhalo – {ex}"); PROBLEMY.append(f"{d} {L}: nahrání selhalo"); odlozit.add(L)
                souhrn.append((d, L, "–", "nahrání selhalo – zkusí příští běh")); continue
            nove = {"videoId": vid, "url": f"https://www.youtube.com/shorts/{vid}", "nahrano": datetime.date.today().isoformat()}
            if kdy: nove = {"zverejneni": kdy.isoformat(timespec="minutes"), **nove}
            e.update(nove); uloz(jpath, L, **nove, playlist=None)   # nové video (i při --znovu) ještě v playlistu není
            stav = f"naplánováno na {kdy.strftime('%d. %m. %Y %H:%M')} ({kdy.tzinfo})" if kdy else "nahráno"
            try:
                p = playlist(token, L)
                if p is not None: stav += ", " + zarad(token, p, vid, evidovana(L))
            except Kvota: stav += ", do playlistu nezařazeno (kvóta) – doplní příští běh"; PROBLEMY.append(f"{d} {L}: playlist")
            except HttpChyba as ex: stav += f", do playlistu nezařazeno (HTTP {ex.code}) – doplní příští běh"; PROBLEMY.append(f"{d} {L}: playlist"); print("   " + str(ex))
            print(f"✅ {d} {L}: {e['url']} ({stav})"); souhrn.append((d, L, e["url"], stav))

    for L in udrzovat:                               # 3) pořadí a závěrečný stav
        if not CFG["jazyky"][L].get("playlist"): continue
        try: stav = serad(token, L)
        except Kvota: stav = "pořadí neověřeno – kvóta vyčerpaná, dokončí příští běh"; PROBLEMY.append(f"{L}: pořadí")
        except HttpChyba as ex: stav = f"řazení selhalo (HTTP {ex.code})"; PROBLEMY.append(f"{L}: pořadí"); print("   " + str(ex))
        print(f"📃 {L}: {stav}"); souhrn.append(("", L, "playlist", stav))
    print(f"(spotřeba kvóty tohoto běhu ≈ {STAV['jednotky']} jednotek z 10 000 denně; nahrávání má vlastní limit)")
    if PROBLEMY: print("⚠️  Nedokončeno: " + "; ".join(PROBLEMY))

    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write("| Díl | Jazyk | Video | Stav |\n|---|---|---|---|\n")
            f.writelines(f"| {d} | {L} | {u} | {' '.join(s.split()).replace('|', '/')[:220]} |\n" for d, L, u, s in souhrn)
            f.write(f"\nSpotřeba kvóty ≈ {STAV['jednotky']} jednotek.\n")
            if PROBLEMY: f.write("\n**Nedokončeno:** " + "; ".join(PROBLEMY) + " – dodělá příští běh (workflow běží i jednou denně).\n")
            elif plan and naplanovat: f.write("\nVidea se zveřejní sama v naplánovaný čas – v YouTube Studiu jim jen nastavte související video.\n")
            elif plan and not verejne: f.write("\nVidea jsou **soukromá** – zveřejněte je v YouTube Studiu (a nastavte související video).\n")
    return 1 if PROBLEMY else 0

if __name__ == "__main__":
    sys.exit(main())
