"""Díl 09 – složení z generovaných klipů: pozadí = klipy (přečasované na délku scény),
přes ně popisky a ukazatel průběhu ve stylu série, zvuk = hlas z ElevenLabs.
Chybí-li klip scény (klipy/V<n>.mp4), použije se pomalý průlet mezi klíčovými snímky.

  python3 make.py preview          → prev_<jazyk>.png (náhled všech scén)
  python3 make.py build [cs en es hi] → hotová MP4 ve složce dílu
  python3 make.py nahled           → nahled-<jazyk>.jpg (540×960)
Vyžaduje ffmpeg, Pillow, numpy, písmo Inter."""
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
here = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(here)
sys.path.insert(0, os.path.join(ROOT, "..", "nastroje"))
from engine import W, H, FPS, font, CY, OR, WH, wrap, fadein, mix, _off, durations

SEG = json.load(open(os.path.join(here, "casovani.json")))
LEAD, TAIL, LAST = 0.25, 0.40, 1.6      # náběh před řečí, dojezd po ní, dojezd poslední scény
XF = 0.35                               # prolínání pozadí mezi scénami (s)
AUDIO = {"cs": "zvuk/hlas-CZ.mp3", "en": "zvuk/voice-EN.mp3", "es": "zvuk/voz-ES.mp3", "hi": "zvuk/awaz-HI.mp3", "pt": "zvuk/voz-PT.mp3"}
OUT = {"cs": "09-projekt-je-strom-CZ.mp4", "en": "09-your-project-is-a-tree-EN.mp4",
       "es": "09-tu-proyecto-es-un-arbol-ES.mp4", "hi": "09-aapka-project-ek-ped-hai-HI.mp4",
       "pt": "09-o-seu-projeto-e-uma-arvore-PT.mp4"}
DEV = os.path.join(ROOT, "..", "nastroje", "pisma", "NotoSansDevanagari-Bold.ttf")   # hindština (devanágarí)

# Pozadí scén: klip V<n> (úsek od–do v sekundách, který se natáhne/zrychlí na délku scény),
# nebo – když klip zatím chybí – průlet mezi dvěma klíčovými snímky.
CLIP_RANGE = {1: (0.0, 8.5), 2: (0.4, 9.6), 3: (1.0, 7.5), 4: (0.3, 9.7), 6: (0.0, 10.0)}
STILLS = {1: ("K01", "K01"), 2: ("K02", "K03"), 3: ("K03", "K04"), 4: ("K05", "K06"),
          5: ("K07", "K08"), 6: ("K08", "K09"), 7: ("K10", "K11"), 8: ("K11", "K12")}

# Popisky: (hlavní, doplněk) – doplněk tyrkysově (AI, správně) nebo oranžově (problém)
T = {
 "cs": [("Projekt = strom", "Bez AI roste pomalu"), ("AI = zavlažování", "Strom roste sám"),
        ("Stříhání = směr", "To je tvoje práce"), ("Škůdci = AI ztratila nit", "Připomeň jí cíl"),
        ("Bez plánu", "přesazuješ pořád dokola"), ("Přesazení = přestavba", "celého projektu"),
        ("Nejdřív plán a test", "zasadíš jen jednou"), ("AI zalévá", "Místo vybíráš ty")],
 "en": [("Project = tree", "Without AI it grows slowly"), ("AI = irrigation", "The tree grows by itself"),
        ("Pruning = direction", "That's your job"), ("Pests = AI lost the thread", "Restate the goal"),
        ("No plan", "endless repotting"), ("Repotting = rebuilding", "the whole project"),
        ("Plan and test first", "plant it just once"), ("AI waters", "You choose the spot")],
 "es": [("Proyecto = árbol", "Sin IA crece despacio"), ("IA = riego", "El árbol crece solo"),
        ("Podar = dar dirección", "Ese es tu trabajo"), ("Plagas = la IA pierde el hilo", "Recuérdale el objetivo"),
        ("Sin plan", "trasplantes sin fin"), ("Trasplantar = rehacer", "todo el proyecto"),
        ("Primero planea y prueba", "planta una sola vez"), ("La IA riega", "El lugar lo eliges tú")],
 "hi": [("प्रोजेक्ट = पेड़", "AI के बिना धीरे बढ़ता है"), ("AI = सिंचाई", "पेड़ खुद बढ़ता है"),
        ("छँटाई = दिशा", "यह आपका काम है"), ("कीड़े = AI भटक गया", "उसे मकसद याद दिलाइए"),
        ("बिना प्लान", "बार-बार गमला बदलना"), ("गमला बदलना = दोबारा बनाना", "पूरा प्रोजेक्ट"),
        ("पहले प्लान और टेस्ट", "पेड़ एक ही बार लगाइए"), ("AI पानी देता है", "जगह आप चुनते हैं")],
 "pt": [("Projeto = árvore", "Sem IA cresce devagar"), ("IA = irrigação", "A árvore cresce sozinha"),
        ("Podar = dar direção", "Esse é o seu trabalho"), ("Pragas = a IA perde o fio", "Lembre o objetivo"),
        ("Sem plano", "transplantes sem fim"), ("Transplantar = refazer", "o projeto inteiro"),
        ("Primeiro planeje e teste", "plante uma vez só"), ("A IA rega", "O lugar quem escolhe é você")]
}
SUBC = [OR, CY, CY, CY, OR, OR, CY, CY]
NS = len(STILLS)

# tmavý přechod nahoře, aby byly popisky čitelné na každém záběru
_g = np.clip(1 - np.arange(H) / 820.0, 0, 1) ** 1.5 * 0.74
SHADE = (1 - _g)[:, None, None].astype(np.float32)

def scene_durs(L):
    return durations(SEG[L] if L in SEG else SEG["en"], LEAD, TAIL, LAST)   # bez nahrávky: náhled s časováním EN

# Sazba: Inter pro latinku a symboly, Noto Sans Devanagari pro hindštinu (Noto nemá latinku ani „=“)
class Fnt:
    def __init__(self, lat, dev=None): self.lat, self.dev = lat, dev

def _isdev(c): return "\u0900" <= c <= "\u097f" or "\ua8e0" <= c <= "\ua8ff" or c in "\u200c\u200d"

def runs(txt):
    out = []
    for c in txt:
        k = (out[-1][0] if out else False) if c == " " else _isdev(c)
        if out and out[-1][0] == k: out[-1][1] += c
        else: out.append([k, c])
    return out

def tlen(d, txt, F):
    if not F.dev: return d.textlength(txt, font=F.lat)
    return sum(d.textlength(s, font=F.dev if k else F.lat) for k, s in runs(txt))

def tdraw(d, x, y, txt, F, fill):
    if not F.dev: d.text((x, y), txt, font=F.lat, fill=fill); return
    base = y + F.lat.getmetrics()[0]                       # společná účaří
    for k, s in runs(txt):
        f = F.dev if k else F.lat
        d.text((x, base), s, font=f, fill=fill, anchor="ls"); x += d.textlength(s, font=f)

def fonts(L):
    if L == "hi":
        return (Fnt(font("b", 82), ImageFont.truetype(DEV, 84)), Fnt(font("b", 58), ImageFont.truetype(DEV, 60)))
    return Fnt(font("x", 82)), Fnt(font("b", 58))

def wrap2(d, txt, F, maxw):
    """Zalomení nadpisu: nejdřív za „=“, jinak na dva co nejvyrovnanější řádky."""
    if tlen(d, txt, F) <= maxw: return [txt]
    if " = " in txt:
        a, b = txt.split(" = ", 1); ls = [a + " =", b]
        if all(tlen(d, l, F) <= maxw for l in ls): return ls
    words = txt.split(); best = None
    for i in range(1, len(words)):
        ls = [" ".join(words[:i]), " ".join(words[i:])]
        m = max(tlen(d, l, F) for l in ls)
        if best is None or m < best[0]: best = (m, ls)
    return best[1] if best else [txt]

_ov_cache = {}
def overlay(L, si, t, dur):
    """Průhledná vrstva s popisky scény (s náběhem a dozvukem jako v sérii)."""
    a1, a2 = fadein(t, 0.15, 0.45), fadein(t, 0.75, 0.45)
    out = min(1.0, max(0.0, (dur - t) / 0.25))
    key = (L, si, round(a1, 2), round(a2, 2), round(out, 2))
    if key in _ov_cache: return _ov_cache[key]
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    big, small = T[L][si]
    fb, fs = fonts(L)
    ls = wrap2(d, big, fb, 940); y = 190
    for i, l in enumerate(ls):
        tdraw(d, (W - tlen(d, l, fb)) / 2, y + i * 96 + _off(a1), l, fb, mix(WH, a1 * out))
    y2 = y + len(ls) * 96 + 20
    for i, l in enumerate(wrap2(d, small, fs, 940)):
        tdraw(d, (W - tlen(d, l, fs)) / 2, y2 + i * 70 + _off(a2), l, fs, mix(SUBC[si], a2 * out))
    A = im.getchannel("A")
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # tmavý stín pod textem (čitelnost na světlé koruně)
    sh.putalpha(A.filter(ImageFilter.GaussianBlur(7)).point(lambda v: min(255, int(v * 0.85))))
    gl = im.resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(9)).resize((W, H), Image.BILINEAR)
    gl.putalpha(gl.getchannel("A").point(lambda v: min(255, int(v * 0.35))))
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0)); base.alpha_composite(sh); base.alpha_composite(gl); base.alpha_composite(im)
    arr = np.asarray(base).astype(np.float32)
    res = (arr[..., :3], arr[..., 3:4] / 255.0)
    if a1 == a2 == out == 1:        # ustálená vrstva scény – jen ta se ukládá (šetří paměť)
        _ov_cache.clear(); _ov_cache[key] = res
    return res

def _cover(img, scale=1.0):
    w, h = img.size; s = max(W / w, H / h) * scale
    return img.resize((int(round(w * s)), int(round(h * s))), Image.LANCZOS)

def still_frames(n, a, b):
    """Průlet: pomalé přiblížení a prolnutí ze snímku a do snímku b."""
    A = _cover(Image.open(os.path.join(ROOT, "obrazky", a + ".jpg")).convert("RGB"), 1.08)
    B = A if a == b else _cover(Image.open(os.path.join(ROOT, "obrazky", b + ".jpg")).convert("RGB"), 1.08)
    for k in range(n):
        u = k / max(1, n - 1); z = 1.08 - 0.06 * u          # přiblížení o 6 %
        def crop(im):
            cw, ch = W * 1.08 / z, H * 1.08 / z
            x0, y0 = (im.width - cw) / 2, (im.height - ch) / 2
            return np.asarray(im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)), dtype=np.float32)
        m = min(1, max(0, (u - 0.40) / 0.35)); m = m * m * (3 - 2 * m)
        fa = crop(A)
        yield fa if m <= 0 or a == b else (fa * (1 - m) + crop(B) * m if m < 1 else crop(B))

def clip_frames(n, path, a, b):
    """Úsek a–b klipu přečasovaný na n snímků (30 fps, 1080×1920, bez zvuku)."""
    f = (n / FPS) / (b - a)
    cmd = ["ffmpeg", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", path, "-an",
           "-vf", f"setpts={f:.5f}*PTS,fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL); last = None
    try:
        for _ in range(n):
            buf = p.stdout.read(W * H * 3)
            if len(buf) == W * H * 3: last = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
            yield last
    finally:
        p.kill(); p.stdout.close(); p.wait()

def bg_frames(si, n):
    v = os.path.join(ROOT, "klipy", f"V{si + 1}.mp4")
    if os.path.exists(v):
        a, b = CLIP_RANGE.get(si + 1, (0.0, float(subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v]))))
        return clip_frames(n, v, a, b)
    return still_frames(n, *STILLS[si + 1])

def compose(L, bg, si, t, dur, Tg, TOTAL):
    rgb, al = overlay(L, si, t, dur)
    img = bg * SHADE
    img = img * (1 - al) + rgb * al
    out = np.clip(img, 0, 255).astype(np.uint8)
    out[0:10, :] = (out[0:10, :].astype(np.float32) * 0.88 + 255 * 0.12).astype(np.uint8)
    out[0:10, :int(W * Tg / TOTAL)] = CY
    return out

def frames(L):
    D = scene_durs(L); N = [int(round(x * FPS)) for x in D]; NX = int(round(XF * FPS))
    TOTAL = sum(N) / FPS; tail = []; g = 0
    for si in range(NS):
        extra = NX if si < NS - 1 else 0
        cur = []
        for k, bg in enumerate(bg_frames(si, N[si] + extra)):
            if k < N[si]:
                if si > 0 and k < len(tail):
                    m = (k + 1) / (len(tail) + 1); bg = tail[k] * (1 - m) + bg * m
                yield compose(L, bg, si, k / FPS, D[si], g / FPS, TOTAL); g += 1
            else: cur.append(bg)
        tail = cur

def audio(L, wav):
    D = scene_durs(L); src = os.path.join(ROOT, AUDIO[L]); parts = []
    for i, (b, e) in enumerate(SEG[L]):
        a = f"/tmp/09_{L}_a{i}.wav"; parts.append(a)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af",
            f"atrim=start={b - 0.03}:end={e + 0.08},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,"
            f"afade=t=out:st={e - b + 0.06}:d=0.05,adelay={int((LEAD - 0.03) * 1000)}|{int((LEAD - 0.03) * 1000)},"
            f"apad=whole_dur={int(round(D[i] * FPS)) / FPS}", "-ar", "48000", "-ac", "2", a], check=True)
    open(f"/tmp/09_{L}_a.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"/tmp/09_{L}_a.txt",
                    "-c:a", "pcm_s16le", wav], check=True)

def build(L):
    vid, wav = f"/tmp/09_{L}_v.mp4", f"/tmp/09_{L}_a.wav"
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "25", "-pix_fmt", "yuv420p", vid],
        stdin=subprocess.PIPE)
    for fr in frames(L): p.stdin.write(fr.tobytes())
    p.stdin.close(); assert p.wait() == 0
    audio(L, wav)
    out = os.path.join(ROOT, OUT[L])
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", vid, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], check=True)
    print("hotovo:", out, f"{sum(scene_durs(L)):.1f} s")

def preview(L):
    """Jeden snímek z každé scény (v 70 % délky) vedle sebe, zmenšeně."""
    D = scene_durs(L); N = [int(round(x * FPS)) for x in D]; TOTAL = sum(N) / FPS; tiles = []
    for si in range(NS):
        k = int(N[si] * 0.7); bg = None
        for j, fr in enumerate(bg_frames(si, N[si])):
            if j == k: bg = fr; break
        img = compose(L, bg, si, k / FPS, D[si], (sum(N[:si]) + k) / FPS, TOTAL)
        tiles.append(Image.fromarray(img).resize((360, 640), Image.LANCZOS))
    sheet = Image.new("RGB", (360 * NS, 640)); [sheet.paste(t, (360 * i, 0)) for i, t in enumerate(tiles)]
    sheet.save(os.path.join(here, f"prev_{L}.png"))

THUMB = {"cs": ("Projekt = strom", "Jak pracovat s AI"), "en": ("Project = tree", "How to work with AI"),
         "es": ("Proyecto = árbol", "Cómo trabajar con IA"), "hi": ("प्रोजेक्ट = पेड़", "AI के साथ कैसे काम करें"),
         "pt": ("Projeto = árvore", "Como trabalhar com IA")}

def nahled(L):
    """Náhled 540×960: plodící jabloň (K12) s nadpisem dílu."""
    T[L].append(THUMB[L]); SUBC.append(CY)
    bg = next(still_frames(1, "K12", "K12"))
    img = compose(L, bg, len(T[L]) - 1, 5.0, 10.0, 0, 1)
    img[0:10, :] = CY
    Image.fromarray(img).resize((540, 960), Image.LANCZOS).save(os.path.join(ROOT, f"nahled-{L}.jpg"), quality=88)
    T[L].pop(); SUBC.pop()

if __name__ == "__main__":
    mode = sys.argv[1]; langs = sys.argv[2:] or ["cs", "en", "es", "hi", "pt"]
    for L in langs: {"preview": preview, "build": build, "nahled": nahled}[mode](L)
