# Naučná videa

Krátká naučná videa (shorts / reels) o tom, jak AI opravdu funguje. Cílem je **osvěta, ne reklama**: ve videích se nezmiňuje kniha, autor ani konkrétní značky – mluví se obecně o „AI“.

## ▶️ Sledovat na YouTube

- 🇨🇿 **Česky:** [playlist na YouTube](https://www.youtube.com/playlist?list=PLNpxYtAHyLcE)
- 🇬🇧 **English:** [YouTube playlist](https://www.youtube.com/playlist?list=PLVOwx6a35k64)
- 🇪🇸 **Español:** [playlist en YouTube](https://www.youtube.com/playlist?list=PLey5e-5qs38Y)
- 🇮🇳 **हिन्दी:** [YouTube प्लेलिस्ट](https://www.youtube.com/playlist?list=PLGM_GEl_OKnE)
- 🇧🇷 **Português:** [playlist no YouTube](https://www.youtube.com/playlist?list=PLHxugCKbRb9o)

## Pravidla série

- **Pět jazyků:** každé video vzniká v 🇨🇿 **češtině**, 🇬🇧 **angličtině**, 🇪🇸 **španělštině**, 🇮🇳 **hindštině** (vykání आप) a 🇧🇷 **brazilské portugalštině** (você). Španělské, hindské a portugalské verze starších dílů vznikly dodatečně – texty jsou v [spanelske-texty-01-08.md](spanelske-texty-01-08.md), [hindske-texty-01-08.md](hindske-texty-01-08.md) a [portugalske-texty-01-09.md](portugalske-texty-01-09.md); od dílu 10 má každý díl texty ve svém `texty.md`. Kde česká analogie v jiném jazyce nefunguje, používá se vlastní (párek v rohlíku → peanut butter and jelly → café con leche → रोटी, कपड़ा और मकान → arroz e feijão).
- **Hlasy (ElevenLabs, tarif Creator)** – namlouvá je workflow **Namluvit** ([návod](nastroje/elevenlabs/NAVOD.md)); ID a nastavení v [`nastroje/elevenlabs/hlasy.json`](nastroje/elevenlabs/hlasy.json):
  - 🇨🇿 **Kuba – Czech Social Media**
  - 🇬🇧 **George – Warm, Captivating Storyteller**
  - 🇪🇸 **Brian C – Clean, professional, warm** (latinskoamerická španělština)
  - 🇮🇳 **Viraj – Rich, Confident and Expressive** (hindština; text pro hlas píše AI jako „एआई“, popisky sází engine kombinací Inter a `nastroje/pisma/NotoSansDevanagari-Bold.ttf`)
  - 🇧🇷 **Zozo** (brazilská portugalština)
- **Namlouvá se jen mluvený text**, bez čísel scén a tabulek. Scény stačí oddělit prázdným řádkem – časování scén i slov se vezme z časů písmen, které vrátí ElevenLabs (`nastroje/casy.py`).
- **Formát:** na výšku 1080 × 1920, 30 fps, 30–55 s, texty na obrazovce odpovídají namluvenému.
- **Generované záběry (od dílu 09):** klíčové snímky z generátoru obrázků → videoklipy v Gemini → hlas → složení s popisky a ukazatelem průběhu. Postup je ve [scénáři dílu 09](09-projekt-je-strom/scenar.md).
- **Design:** tmavé pozadí s pohyblivými světelnými skvrnami (modrá, fialová, oranžová), jemná záře textu, ukazatel průběhu nahoře, písmo Inter.

## Díly

| # | Téma | 🇨🇿 | 🇬🇧 | 🇪🇸 | 🇮🇳 | 🇧🇷 | Stav |
|---|---|---|---|---|---|---|---|
| 01 | [Jak „myslí“ AI](01-jak-mysli-ai/) | [video](01-jak-mysli-ai/01-jak-mysli-ai-CZ.mp4) | [video](01-jak-mysli-ai/01-how-ai-thinks-EN.mp4) | [video](01-jak-mysli-ai/01-como-piensa-la-ia-ES.mp4) | [video](01-jak-mysli-ai/01-ai-kaise-sochta-hai-HI.mp4) | [video](01-jak-mysli-ai/01-como-a-ia-pensa-PT.mp4) | ✅ hotovo |
| 02 | [Mozek spojený provázkem](02-mozek-spojeny-provazkem/) | [video](02-mozek-spojeny-provazkem/02-mozek-spojeny-provazkem-CZ.mp4) | [video](02-mozek-spojeny-provazkem/02-brain-tied-with-string-EN.mp4) | [video](02-mozek-spojeny-provazkem/02-un-cerebro-atado-con-un-cordel-ES.mp4) | [video](02-mozek-spojeny-provazkem/02-dhaage-se-juda-dimaag-HI.mp4) | [video](02-mozek-spojeny-provazkem/02-cerebro-amarrado-com-barbante-PT.mp4) | ✅ hotovo |
| 03 | [Nech AI postavit kalkulačku](03-nech-ai-postavit-kalkulacku/) | [video](03-nech-ai-postavit-kalkulacku/03-nech-ai-postavit-kalkulacku-CZ.mp4) | [video](03-nech-ai-postavit-kalkulacku/03-have-ai-build-the-calculator-EN.mp4) | [video](03-nech-ai-postavit-kalkulacku/03-que-la-ia-te-construya-la-calculadora-ES.mp4) | [video](03-nech-ai-postavit-kalkulacku/03-ai-se-calculator-banwaiye-HI.mp4) | [video](03-nech-ai-postavit-kalkulacku/03-peca-para-a-ia-construir-a-calculadora-PT.mp4) | ✅ hotovo |
| 04 | [Kecálek vs. vidí za roh](04-kecalek-vs-vidi-za-roh/) | [video](04-kecalek-vs-vidi-za-roh/04-kecalek-vs-vidi-za-roh-CZ.mp4) | [video](04-kecalek-vs-vidi-za-roh/04-chatterbox-vs-sees-around-corners-EN.mp4) | [video](04-kecalek-vs-vidi-za-roh/04-parlanchin-vs-ve-mas-alla-ES.mp4) | [video](04-kecalek-vs-vidi-za-roh/04-baatooni-ya-door-tak-dekhne-wala-HI.mp4) | [video](04-kecalek-vs-vidi-za-roh/04-tagarela-vs-enxerga-longe-PT.mp4) | ✅ hotovo |
| 05 | [AI je zesilovač](05-ai-je-zesilovac/) | [video](05-ai-je-zesilovac/05-ai-je-zesilovac-CZ.mp4) | [video](05-ai-je-zesilovac/05-ai-is-an-amplifier-EN.mp4) | [video](05-ai-je-zesilovac/05-la-ia-es-un-amplificador-ES.mp4) | [video](05-ai-je-zesilovac/05-ai-ek-amplifier-hai-HI.mp4) | [video](05-ai-je-zesilovac/05-a-ia-e-um-amplificador-PT.mp4) | ✅ hotovo |
| 06 | [Co je AI agent](06-co-je-ai-agent/) | [video](06-co-je-ai-agent/06-co-je-ai-agent-CZ.mp4) | [video](06-co-je-ai-agent/06-what-is-an-ai-agent-EN.mp4) | [video](06-co-je-ai-agent/06-que-es-un-agente-de-ia-ES.mp4) | [video](06-co-je-ai-agent/06-ai-agent-kya-hai-HI.mp4) | [video](06-co-je-ai-agent/06-o-que-e-um-agente-de-ia-PT.mp4) | ✅ hotovo |
| 07 | [Naše „nic“ není důkaz](07-nase-nic-neni-dukaz/) | [video](07-nase-nic-neni-dukaz/07-nase-nic-neni-dukaz-CZ.mp4) | [video](07-nase-nic-neni-dukaz/07-our-nothing-is-not-proof-EN.mp4) | [video](07-nase-nic-neni-dukaz/07-nuestra-nada-no-es-una-prueba-ES.mp4) | [video](07-nase-nic-neni-dukaz/07-hamara-kuch-nahin-saboot-nahin-HI.mp4) | [video](07-nase-nic-neni-dukaz/07-o-nosso-nada-nao-e-prova-PT.mp4) | ✅ hotovo |
| 08 | [Firma v Gitu](08-firma-v-gitu/) | [video](08-firma-v-gitu/08-firma-v-gitu-CZ.mp4) | [video](08-firma-v-gitu/08-a-company-in-git-EN.mp4) | [video](08-firma-v-gitu/08-una-empresa-en-git-ES.mp4) | [video](08-firma-v-gitu/08-git-mein-ek-company-HI.mp4) | [video](08-firma-v-gitu/08-uma-empresa-no-git-PT.mp4) | ✅ hotovo |
| 09 | [Projekt je strom](09-projekt-je-strom/) | [video](09-projekt-je-strom/09-projekt-je-strom-CZ.mp4) | [video](09-projekt-je-strom/09-your-project-is-a-tree-EN.mp4) | [video](09-projekt-je-strom/09-tu-proyecto-es-un-arbol-ES.mp4) | [video](09-projekt-je-strom/09-aapka-project-ek-ped-hai-HI.mp4) | [video](09-projekt-je-strom/09-o-seu-projeto-e-uma-arvore-PT.mp4) | ✅ hotovo |
| 10 | [Normy jako rady zdarma](10-normy-jako-rady-zdarma/) | [video](10-normy-jako-rady-zdarma/10-normy-jako-rady-zdarma-CZ.mp4) | [video](10-normy-jako-rady-zdarma/10-standards-as-free-advice-EN.mp4) | [video](10-normy-jako-rady-zdarma/10-normas-como-consejos-gratis-ES.mp4) | [video](10-normy-jako-rady-zdarma/10-maanak-muft-salaah-HI.mp4) | [video](10-normy-jako-rady-zdarma/10-normas-como-conselhos-gratis-PT.mp4) | ✅ hotovo |
| 11 | [Proč AI v dlouhém chatu chybuje](11-dlouhy-chat/) | [video](11-dlouhy-chat/11-proc-ai-v-dlouhem-chatu-chybuje-CZ.mp4) | [video](11-dlouhy-chat/11-why-ai-slips-in-long-chats-EN.mp4) | [video](11-dlouhy-chat/11-por-que-la-ia-falla-en-chats-largos-ES.mp4) | [video](11-dlouhy-chat/11-lambi-chat-mein-ai-kyon-chookta-hai-HI.mp4) | [video](11-dlouhy-chat/11-por-que-a-ia-erra-em-chats-longos-PT.mp4) | ✅ hotovo |
| 12 | [Když boti mluví s boty](12-boti-mluvi-s-boty/) | [video](12-boti-mluvi-s-boty/12-kdyz-boti-mluvi-s-boty-CZ.mp4) | [video](12-boti-mluvi-s-boty/12-when-bots-talk-to-bots-EN.mp4) | [video](12-boti-mluvi-s-boty/12-cuando-los-bots-hablan-con-bots-ES.mp4) | [video](12-boti-mluvi-s-boty/12-jab-bots-bots-se-baat-karte-hain-HI.mp4) | [video](12-boti-mluvi-s-boty/12-quando-bots-conversam-com-bots-PT.mp4) | ✅ hotovo |
| 13 | [Myšlení rychlé a pomalé](13-mysleni-rychle-a-pomale/) | [video](13-mysleni-rychle-a-pomale/13-mysleni-rychle-a-pomale-CZ.mp4) | [video](13-mysleni-rychle-a-pomale/13-thinking-fast-and-slow-EN.mp4) | [video](13-mysleni-rychle-a-pomale/13-pensar-rapido-y-despacio-ES.mp4) | [video](13-mysleni-rychle-a-pomale/13-tez-soch-aur-dheemi-soch-HI.mp4) | [video](13-mysleni-rychle-a-pomale/13-pensar-rapido-e-devagar-PT.mp4) | ✅ hotovo |

## Postup výroby dílu

1. Claude napíše mluvený text CZ + EN + ES (tabulka po scénách).
2. Text namluví workflow **Namluvit (ElevenLabs)** – Claude ho spustí zápisem do fronty ve větvi `claude/upravy` ([`nastroje/elevenlabs/NAVOD.md`](nastroje/elevenlabs/NAVOD.md)); dřív namlouval autor ručně a posílal MP3.
3. Claude podle časů slov (nebo přepisu `nastroje/prepis.py`) najde začátky a konce scén a sestaví všechny jazykové verze videa.
4. Claude doplní do složky dílu `youtube.json` (název, popis, štítky pro každý jazyk) a pošle videa autorovi ke kontrole.
5. Autor sloučí pull request do `main` – tím se videa samy nahrají, naplánují (v každém jazyce jedno denně) a zařadí do playlistů; co běh nestihne (např. kvóta YouTube API), dodělá denní běh. V YouTube Studiu jim pak jen nastaví související video. Nastavení a postup: [`nastroje/youtube/NAVOD.md`](nastroje/youtube/NAVOD.md).

Sdílený vzhled (pozadí, písmo, záře, ukazatel průběhu, sestavení s hlasem) je v `nastroje/engine.py`; každý díl od 02 má v `zdroj/` jen vlastní scény a časování. Úseky řeči v nahrávce vypíše `nastroje/intervaly.py`.

Podrobný postup výroby (pro Clauda) je ve skillu [`.claude/skills/naucne-video/SKILL.md`](../.claude/skills/naucne-video/SKILL.md).

---

[← Zpět na knihu](../README.md)
