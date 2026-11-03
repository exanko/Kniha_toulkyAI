# Naučná videa

Krátká naučná videa (shorts / reels) o tom, jak AI opravdu funguje. Cílem je **osvěta, ne reklama**: ve videích se nezmiňuje kniha, autor ani konkrétní značky – mluví se obecně o „AI“.

## Pravidla série

- **Dva jazyky:** každé video vzniká vždy ve dvou verzích – 🇨🇿 **česky** a 🇬🇧 **anglicky**. Kde česká analogie v angličtině nefunguje, používá se vlastní anglická (párek v rohlíku → peanut butter and jelly).
- **Hlasy (ElevenLabs, bezplatný tarif):**
  - 🇨🇿 **Kuba – Czech Social Media**
  - 🇬🇧 **George – Warm, Captivating Storyteller**
- **Do ElevenLabs vkládat jen mluvený text**, bez čísel scén a tabulek. Scény stačí oddělit prázdným řádkem – pauzy se v nahrávce najdou automaticky.
- **Formát:** na výšku 1080 × 1920, 30 fps, 30–40 s, texty na obrazovce odpovídají namluvenému.
- **Design:** tmavé pozadí s pohyblivými světelnými skvrnami (modrá, fialová, oranžová), jemná záře textu, ukazatel průběhu nahoře, písmo Inter.

## Díly

| # | Téma | 🇨🇿 | 🇬🇧 | Stav |
|---|---|---|---|---|
| 01 | [Jak „myslí“ AI](01-jak-mysli-ai/) | [video](01-jak-mysli-ai/01-jak-mysli-ai-CZ.mp4) | [video](01-jak-mysli-ai/01-how-ai-thinks-EN.mp4) | ✅ hotovo |
| 02 | Mozek spojený provázkem – proč si doma neuděláš vlastní ChatGPT | | | 📝 plán |
| 03 | Nech AI vyrobit nástroj – ne počítat data | | | 📝 plán |
| 04 | Kecálek vs. vidí za roh – malé a velké modely | | | 📝 plán |
| 05 | AI je zesilovač – kladné i záporné | | | 📝 plán |
| 06 | Hloupý s nástroji, chytrý bez paměti – co je agent | | | 📝 plán |
| 07 | Naše „nic“ není důkaz – záblesk na sirce | | | 📝 plán |
| 08 | Firma v Gitu za 45 vteřin | | | 📝 plán |

## Postup výroby dílu

1. Claude napíše mluvený text CZ + EN (tabulka po scénách).
2. Autor ho namluví v ElevenLabs (hlasy výše) a pošle MP3.
3. Claude nahrávky přepíše (`nastroje/prepis.py`), najde začátky a konce scén a sestaví obě verze videa.

---

[← Zpět na knihu](../README.md)
