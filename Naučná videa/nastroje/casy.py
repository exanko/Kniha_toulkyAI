"""Časování scén z nahrávky namluvené workflow „Namluvit“ (soubor <hlas>.casy.json s časy písmen).

  python3 casy.py <díl>/zvuk/voz-ES.casy.json            → intervaly scén pro casovani.json
                                                            + každé slovo s hodnotou pro K
Scény = odstavce textu oddělené prázdným řádkem. Začátek a konec scény se zpřesní podle skutečné
řeči v MP3 vedle (stejné jako intervaly.py), časy písmen z ElevenLabs bývají o pár setin volnější.
K u slova = čas slova − začátek řeči scény + 0,35 (pravidlo dílů 02–08; díl 01: + 0,32)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def sceny(path, k_plus=0.35):
    d = json.load(open(path, encoding="utf-8")); a = d["alignment"]
    ch, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
    text = "".join(ch)
    if text != d["text"]: raise SystemExit("text v alignment nesouhlasí s textem nahrávky")
    mp3 = path[:-len(".casy.json")] + ".mp3"
    try:
        from intervaly import intervaly            # skutečné úseky řeči v MP3
        rec = intervaly(mp3)
    except Exception:
        rec = []
    out, i = [], 0
    for p in text.split("\n\n"):
        j = text.index(p, i); s0 = j + len(p) - len(p.lstrip()); k = j + len(p.rstrip()); i = k
        a0, a1 = st[s0], en[k - 1]
        uv = [(s, e) for s, e in rec if a0 - 0.15 <= (s + e) / 2 <= a1 + 0.15]
        s, e = (uv[0][0], uv[-1][1]) if uv else (a0, a1)
        slova = [(m.group(), round(st[s0 + m.start()] - s + k_plus, 2))
                 for m in re.finditer(r"[^\s]+", text[s0:k])]
        out.append({"text": p.strip(), "od": round(s, 2), "do": round(e, 2), "slova": slova})
    return out

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    sc = sceny(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 0.35)
    for n, s in enumerate(sc, 1):
        print(f"\n{n}. [{s['od']:.2f}, {s['do']:.2f}]  " + "  ".join(f"{w} {t:.2f}" for w, t in s["slova"]))
    print("\ncasovani:", json.dumps([[s["od"], s["do"]] for s in sc]))
