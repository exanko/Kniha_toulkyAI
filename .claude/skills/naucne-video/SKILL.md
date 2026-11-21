---
name: naucne-video
description: Výroba dalšího dílu série Naučná videa (česky, anglicky a španělsky, hlasy z ElevenLabs) v repozitáři Kniha_toulkyAI – od mluveného textu přes přepis nahrávky a časování po render, repo a README.
---

# Naučné video – postup výroby dílu

Série krátkých videí na výšku (1080 × 1920, 30 fps, 30–55 s) o tom, jak AI opravdu funguje. Od dílu 09 lze místo animovaných textů použít generované záběry (klíčové snímky → videoklipy v Gemini) – postup je ve `scenar.md` dílu 09. Pravidla série jsou v `Naučná videa/README.md` – přečti je jako první.

## Pevná pravidla

- **Osvěta, ne reklama:** nezmiňovat knihu, autora ani značky (ChatGPT apod.) – obecně „AI“, „jazykový model“.
- **Pět jazyků:** 🇨🇿 česky + 🇬🇧 anglicky + 🇪🇸 španělsky (tykání, latinskoamerická slovní zásoba) + 🇧🇷 brazilsky portugalsky (você, „a gente“; na obrazovce „IA“) + 🇮🇳 hindsky (vykání आप; v textu pro hlas „एआई“ a „गिट“, na obrazovce „AI“ a „Git“; rovné uvozovky). Kde česká analogie nefunguje, vymyslet vlastní (párek v rohlíku → peanut butter and jelly → café con leche → रोटी, कपड़ा और मकान → arroz e feijão). Texty starších dílů: `Naučná videa/spanelske-texty-01-08.md`, `hindske-texty-01-08.md`, `portugalske-texty-01-09.md`; od dílu 10 `NN-nazev/texty.md`. Hindské popisky se píšou do `T["hi"]` jako obyčejné řetězce: kreslicí plocha z `engine.py` (new(), ImageDraw.Draw()) sama sází devanágarí písmem `nastroje/pisma/NotoSansDevanagari-Bold.ttf` a latinku Inter na společné účaří (díl 01 si ji bere z engine.py). Šířky měř `d.textlength` z té plochy; dandu „।“ počítej i v kódu, který dělí věty podle teček (díl 01, scéna 4).
- **Hlasy (ElevenLabs):** CZ **Kuba – Czech Social Media**, EN **George – Warm, Captivating Storyteller**, ES **Brian C – Clean, professional, warm** (latinskoamerická; `zvuk/voz-ES.mp3`), HI **Viraj** (`zvuk/awaz-HI.mp3`), PT **Zozo** (`zvuk/voz-PT.mp3`); ID a nastavení v `Naučná videa/nastroje/elevenlabs/hlasy.json`. Namlouvá workflow **Namluvit**: zapiš úlohy do `nastroje/elevenlabs/fronta.json` (jazyk, text + sekce, vystup) a pushni do `claude/upravy` – za ~1 min přibude ve větvi MP3 a `<název>.casy.json` s časy písmen, výsledek v `vysledek.md` (počkej přes `git ls-remote`, pak fetch). `"kontrola": true` jen ověří klíč a kredity. Postup: `nastroje/elevenlabs/NAVOD.md`. Časování pak z časů písmen: `python3 "Naučná videa/nastroje/casy.py" <díl>/zvuk/voz-ES.casy.json` vypíše řádek pro `casovani.json` (zpřesněný podle skutečné řeči v MP3) a u každého slova hodnotu pro `K` (čas slova − začátek řeči scény + 0,35; pro díl 01 druhý argument 0.32) – přepis přes `prepis.py` tím odpadá.
- **Věcná přesnost:** kategorická tvrzení z knihy, která recenzenti vytkli, ve videu zmírnit (např. „zadání je pro něj svaté“ → „jde přesně tam, kam ho nasměruješ“).
- Claude pracuje ve větvi `claude/upravy`, do `main` jen na výslovný pokyn autora.

## 1. Mluvený text

Napiš text pro všech pět jazyků do `Naučná videa/NN-nazev/texty.md`: nadpis `## cs · 🇨🇿 Česky · <název dílu>` (en, es, hi, pt obdobně) a pod ním blok kódu – **jen mluvený text, scény oddělené prázdným řádkem, bez čísel scén**. 6 scén, 1–3 krátké věty na scénu. Čísla, která hlas může číst špatně, rozepiš slovy (CZ „ISO devět tisíc jedna“, HI „आईएसओ नौ हज़ार एक“). Pak všech pět úloh do fronty Namluvit (`sekce` = kód jazyka, `vystup` = `zvuk/hlas-CZ.mp3`, `voice-EN.mp3`, `voz-ES.mp3`, `awaz-HI.mp3`, `voz-PT.mp3`). Vzor: díly 10–13.

## 2. Nástroje (jednou za session)

- ffmpeg, Pillow, numpy, písmo Inter v `/usr/share/fonts/opentype/inter/` (engine ho očekává tam).
- Přepis: `pip install --break-system-packages sherpa-onnx` a model
  `https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.tar.bz2` (rozbalit do scratchpadu; GitHub je dostupný přes proxy, HuggingFace ne).

## 3. Přepis a časování

**Od dílu 10:** `casovani.json` z časů písmen (`casy.sceny()` pro každý jazyk, viz díly 10–13) a `K` se počítá samo z kotevních slov: v `make.py` slovník `A = {jazyk: {klíč: (scéna od 0, začátek slova[, kolikátý výskyt])}}` a `K = kotvy(<zvuk>.casy.json, A[LANG])` z `nastroje/casy.py` – překlep v kotvě skončí chybou. Postup níže platí pro ručně namluvené starší nahrávky.


1. `python3 "Naučná videa/nastroje/prepis.py" <model> zvuk/hlas-CZ.mp3 cs` (a EN) – ověř, že hlas řekl správný text.
2. `python3 "Naučná videa/nastroje/intervaly.py" zvuk/hlas-CZ.mp3` – seznam úseků řeči `[i]začátek-konec`.
3. Podle přepisu přiřaď úseky ke scénám → `zdroj/casovani.json`: `{"cs": [[začátek, konec], ...], "en": [...]}` (začátek prvního a konec posledního úseku scény).
4. **Klíčové okamžiky** (kdy má v obraze něco naskočit podle toho, kdy to hlas řekne): `lokální čas = čas_v_nahrávce − začátek_scény + 0,35`. Ulož do slovníku `K` v `make.py`.
5. Délky scén počítá `engine.durations()` = 0,35 s náběh + řeč + 0,55 s (poslední scéna 1,4 s).

## 4. Scény (`zdroj/make.py`)

Šablona = díly 10–13 (sdílené kresby v `nastroje/kresby.py`: bubliny, štítky, dokumenty, boti, ozubené kolo, blesk, pečeť; `fit()`/`fitl()` zmenší písmo tak, aby se text vešel ve všech jazycích), starší šablona = díly 02–08. Struktura:
- `sys.path` na `../../nastroje`, `from engine import *` a `from engine import _off`
- `T` = texty na obrazovce pro `cs` / `en` (musí odpovídat namluvenému), `K` = klíčové okamžiky, `D = durations(SEG)`
- funkce `s1(t)…sN(t)`: `im,d=new()`, kreslit přes `ctext`, `lines`, `mix(barva, alfa)`, náběh `fadein(t, čas)`; vrací průhlednou vrstvu
- `SCENES=list(zip(D,[s1,…]))`, na konci `main(SCENES, LANG, složka, náhledové_časy)`
- Barvy: `CY` tyrkys, `MG` fialová, `OR` oranžová, `RD` červená, `WH` bílá, `GR` šedá. Písmo `font("x"|"b"|"sb"|"m", velikost)`.
- Engine řeší pozadí (pohyblivé světelné skvrny + zrno), záři, prolínání scén a ukazatel průběhu – v dílu se nekreslí.

## 5. Kontrola před renderem

`LANG_V=cs python3 make.py preview` a `LANG_V=en …` → `prev_<lang>_<scéna>.png`. Slož je do jednoho náhledového obrázku a **prohlédni**: přetékající text (hlavně delší angličtina – zmenšit písmo pro `en`), překrývání prvků, pořadí vrstev. Teprve pak render.

## 6. Render

`python3 zdroj/build.py` – vyrenderuje scény obou jazyků, z nahrávky vystřihne úseky podle `casovani.json` a složí výsledná MP4. Trvá několik minut: spouštěj na pozadí (`nohup … &`) a čekej na hotovo. Pak `prepis.py` na hotové video jako kontrola a pár snímků přes `ffmpeg -ss`.

## 7. Repo a předání

- Složka dílu: `NN-nazev/` s `NN-nazev-CZ.mp4`, `NN-english-name-EN.mp4`, `nahled-cs.jpg`, `nahled-en.jpg` (540 × 960), `zvuk/hlas-CZ.mp3`, `zvuk/voice-EN.mp3`, `zdroj/` (make.py, build.py, casovani.json) a `README.md` (tabulka videí a náhledů, myšlenka, mluvený text po scénách).
- V `Naučná videa/README.md` přepni řádek dílu na ✅ hotovo s odkazy.
- Vytvoř `NN-nazev/youtube.json` podle vzoru `09-projekt-je-strom/youtube.json` (pro každý jazyk soubor, název ≤ 100 znaků, popis s #shorts, štítky; bez `videoId`). U dílů 01–08 jen nové jazyky (CZ/EN byly nahrané ručně a nemají ID). Nová jazyková verze staršího dílu: doplnit `T["xx"]` a `K["xx"]` v `zdroj/make.py` (u dílů 02–08 platí body 4–5 výše; jen díl 01 má vlastní kopii enginu: K = 0,32 s + čas slova od začátku řeči scény, délka scény = řeč + 0,9 s, poslední + 1,75 s), časování do `casovani.json`, zdroj a výstup do `build.py` (`python3 build.py xx` vyrenderuje jen daný jazyk), změřit šířky textů (≤ 1000 px, jinak rozdělit na dva řádky nebo zkrátit), náhled ze stejné scény jako CZ/EN: `python3 nastroje/nahled.py <díl> xx <scéna> [čas]`. Ověř `python3 "Naučná videa/nastroje/youtube/nahraj.py" NN --zkouska`. Videa pošli autorovi ke kontrole; po jeho sloučení do `main` se workflow **Nahrát na YouTube** spustí samo, nahraje a naplánuje (jedno video denně v každém jazyce, čas v `kanal.json`) a ID i termíny zapíše do `youtube.json`. Postup: `Naučná videa/nastroje/youtube/NAVOD.md`.
- Commit do `claude/upravy`, push, poslat obě videa autorovi a hned přiložit mluvený text dalšího dílu.
