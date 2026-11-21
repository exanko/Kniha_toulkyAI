# Namlouvání přes ElevenLabs (workflow „Namluvit“)

Claude zapíše do [`fronta.json`](fronta.json) ve větvi `claude/upravy`, co se má namluvit, a pushne ji. Tím se na GitHubu sám spustí workflow **Namluvit (ElevenLabs)**. Ten pošle texty do API ElevenLabs a vrátí do téže větve:

- MP3 (stejný hlas a nastavení jako při ručním namlouvání – [`hlasy.json`](hlasy.json)),
- vedle ní `<název>.casy.json` s časy jednotlivých písmen (podle nich Claude časuje popisky),
- [`vysledek.md`](vysledek.md) se záznamem posledního běhu a zbývajícími kredity.

Hotové úlohy z fronty zmizí, nepovedené v ní zůstanou. Jeden běh namluví nejvýš 20 000 znaků (pojistka proti omylu). Existující MP3 se nepřepíše, pokud úloha nemá `"znovu": true`.

## Nastavení (jednou)

1. **Placený tarif ElevenLabs** (Starter a výš) – hlasy z knihovny jdou přes API jen s ním.
2. **API klíč:** ElevenLabs → Developers → API Keys → Create Key. Název třeba `GitHub – Kniha`. Omezení:
   - přístup jen k **Text to Speech** (a případně **User: Read**, aby se ve výsledku ukazovaly zbývající kredity),
   - měsíční limit kreditů, třeba 30 000.
3. **Tajemství v GitHubu:** repozitář → Settings → Secrets and variables → Actions → New repository secret → název `ELEVENLABS_API_KEY`, hodnota = klíč. Do chatu ho neposílejte.
4. **ID hlasů** v `hlasy.json` (nejsou tajná) – doplní Claude.

## Fronta

```json
{"ulohy": [
  {"jazyk": "es", "text": "Naučná videa/spanelske-texty-01-08.md", "sekce": "07",
   "vystup": "Naučná videa/07-nase-nic-neni-dukaz/zvuk/voz-ES.mp3"}
]}
```

- `text` – soubor s textem; se `sekce` se vezme první blok ``` pod nadpisem `## 07 …`,
- `vystup` – kam uložit MP3 (jen uvnitř `Naučná videa/`),
- `znovu` – `true` = namluvit znovu, i když MP3 už existuje.

Ručně jde workflow spustit přes Actions → Namluvit (ElevenLabs) → Run workflow → větev `claude/upravy` (na `main` neběží).
