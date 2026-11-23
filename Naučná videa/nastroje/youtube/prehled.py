"""Přehled kanálu jen pro čtení: jazyk kanálu, jazyky všech nahraných videí a playlistů.

  python3 prehled.py        (přihlašovací údaje YT_* jako u nahraj.py; stojí jednotky kvóty, nic nemění)

U videí evidovaných v repu porovná jazyk názvu (defaultLanguage) a zvuku (defaultAudioLanguage)
s kódem jazyka z kanal.json; nesoulad označí ⚠️. Videa, která repo nezná (nahraná ručně),
jen vypíše – jazyk jim je potřeba zkontrolovat podle názvu."""
import os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nahraj as N

def main():
    token = N.access_token()
    ch = N.api("GET", f"{N.API}/youtube/v3/channels?part=snippet,brandingSettings,contentDetails&mine=true", token)["items"][0]
    sn, br = ch["snippet"], ch.get("brandingSettings", {}).get("channel", {})
    print(f"Kanál „{sn['title']}“: jazyk kanálu {sn.get('defaultLanguage') or br.get('defaultLanguage') or '–'}, země {sn.get('country') or br.get('country') or '–'}")

    znam = {}                                         # videoId → (jazyk v repu, díl)
    for L in N.CFG["jazyky"]:
        for v, c in N.evidovana(L).items(): znam[v] = (L, c)
    ids = [v for _, v in N.polozky(token, ch["contentDetails"]["relatedPlaylists"]["uploads"])]
    videa = []
    for i in range(0, len(ids), 50):
        q = urllib.parse.quote(",".join(ids[i:i + 50]))
        videa += N.api("GET", f"{N.API}/youtube/v3/videos?part=snippet,status,localizations&id={q}", token).get("items", [])
    print(f"\nVidea na kanálu: {len(videa)} (z toho v repu {sum(v['id'] in znam for v in videa)})")
    print("díl jaz | id          | stav      | zveřejnění       | jazyk názvu | jazyk zvuku | název")
    nesoulad = 0
    def klic(v): return (znam.get(v["id"], ("~", 99))[0], znam.get(v["id"], ("~", 99))[1], v["snippet"].get("publishedAt", ""))
    for v in sorted(videa, key=klic):
        s, st = v["snippet"], v["status"]
        kdy = (st.get("publishAt") or s.get("publishedAt") or "")[:16].replace("T", " ")
        dl, da = s.get("defaultLanguage") or "–", s.get("defaultAudioLanguage") or "–"
        if v["id"] in znam:
            L, c = znam[v["id"]]; ocek = N.CFG["jazyky"][L]["kod"]; kde = f"{c:02d}  {L}"
            chyba = dl != ocek or da != ocek
        else: kde, chyba = "??  ??", dl == "–" or da == "–"
        nesoulad += chyba
        lok = ",".join(sorted(v.get("localizations", {})))
        print(f"{'⚠️ ' if chyba else ''}{kde} | {v['id']} | {st['privacyStatus']:<9} | {kdy:<16} | {dl:<11} | {da:<11} | {s['title'][:60]}"
              + (f" | překlady: {lok}" if lok else ""))
        for jl, t in sorted(v.get("localizations", {}).items()):     # přeložené názvy, když se liší od výchozího
            if t.get("title") and t["title"] != s["title"]: print(f"      název [{jl}]: {t['title'][:90]}")

    print("\nPlaylisty:")
    pls = {L: x["playlist"] for L, x in N.CFG["jazyky"].items() if x.get("playlist")}
    q = urllib.parse.quote(",".join(pls.values()))
    info = {p["id"]: p for p in N.api("GET", f"{N.API}/youtube/v3/playlists?part=snippet,localizations,status&id={q}", token).get("items", [])}
    for L, pid in pls.items():
        p = info.get(pid)
        if not p: print(f"   {L}: playlist {pid} nenalezen"); continue
        dl = p["snippet"].get("defaultLanguage") or "–"; ocek = N.CFG["jazyky"][L]["kod"]
        chyba = dl != "–" and dl.split("-")[0] != ocek.split("-")[0]
        lok = ",".join(sorted(p.get("localizations", {})))
        print(f"{'⚠️ ' if chyba else '   '}{L}: „{p['snippet']['title']}“ · jazyk {dl} · {p['status']['privacyStatus']}" + (f" · překlady: {lok}" if lok else ""))
    print(f"\nNesoulad u videí: {nesoulad} · spotřeba kvóty ≈ {N.STAV['jednotky']} jednotek")

if __name__ == "__main__":
    main()
