---
name: naucne-video
description: Výroba dalšího dílu série Naučná videa (česky + anglicky, hlasy z ElevenLabs) v repozitáři Kniha_toulkyAI – od mluveného textu přes přepis nahrávky a časování po render, repo a README.
---

# Naučné video – postup výroby dílu

Série krátkých videí na výšku (1080 × 1920, 30 fps, 30–45 s) o tom, jak AI opravdu funguje. Pravidla série jsou v `Naučná videa/README.md` – přečti je jako první.

## Pevná pravidla

- **Osvěta, ne reklama:** nezmiňovat knihu, autora ani značky (ChatGPT apod.) – obecně „AI“, „jazykový model“.
- **Vždy dva jazyky:** 🇨🇿 česky + 🇬🇧 anglicky. Kde česká analogie nefunguje, vymyslet anglickou (párek v rohlíku → peanut butter and jelly).
- **Hlasy (ElevenLabs, bezplatný tarif – namlouvá autor):** CZ **Kuba – Czech Social Media**, EN **George – Warm, Captivating Storyteller**.
- **Věcná přesnost:** kategorická tvrzení z knihy, která recenzenti vytkli, ve videu zmírnit (např. „zadání je pro něj svaté“ → „jde přesně tam, kam ho nasměruješ“).
- Claude pracuje ve větvi `claude/upravy`, do `main` jen na výslovný pokyn autora.

## 1. Mluvený text

Napiš text pro CZ i EN jako dva bloky kódu – **jen mluvený text, scény oddělené prázdným řádkem, bez čísel scén** (ElevenLabs jinak čte i čísla). 6–7 scén, 1–3 krátké věty na scénu. Stručně popiš, co bude v obraze. Ulož do `Naučná videa/NN-nazev/scenar.md` se stavem „čeká na namluvení“.

## 2. Nástroje (jednou za session)

- ffmpeg, Pillow, numpy, písmo Inter v `/usr/share/fonts/opentype/inter/` (engine ho očekává tam).
- Přepis: `pip install --break-system-packages sherpa-onnx` a model
  `https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.tar.bz2` (rozbalit do scratchpadu; GitHub je dostupný přes proxy, HuggingFace ne).

## 3. Přepis a časování

1. `python3 "Naučná videa/nastroje/prepis.py" <model> zvuk/hlas-CZ.mp3 cs` (a EN) – ověř, že hlas řekl správný text.
2. `python3 "Naučná videa/nastroje/intervaly.py" zvuk/hlas-CZ.mp3` – seznam úseků řeči `[i]začátek-konec`.
3. Podle přepisu přiřaď úseky ke scénám → `zdroj/casovani.json`: `{"cs": [[začátek, konec], ...], "en": [...]}` (začátek prvního a konec posledního úseku scény).
4. **Klíčové okamžiky** (kdy má v obraze něco naskočit podle toho, kdy to hlas řekne): `lokální čas = čas_v_nahrávce − začátek_scény + 0,35`. Ulož do slovníku `K` v `make.py`.
5. Délky scén počítá `engine.durations()` = 0,35 s náběh + řeč + 0,55 s (poslední scéna 1,4 s).

## 4. Scény (`zdroj/make.py`)

Šablona = kterýkoli díl od 02 (`02-…/zdroj/make.py`). Struktura:
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
- Commit do `claude/upravy`, push, poslat obě videa autorovi a hned přiložit mluvený text dalšího dílu.
