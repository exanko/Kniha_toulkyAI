# 2. Přemýšlení

LLM si nejprve vede diskusi sám se sebou, než odpoví. Netuším, jak to funguje, ale je to zajímavé.

Pak jsem zjistil, že Gemini je součástí vyhledávání Google a umí programovat weby a webové kalkulačky. Vytvořil jsem jich celou hromadu.

Gemini pod firemním účtem toho umí víc. Zjistil jsem, že je lepší nenechávat AI zpracovávat data, ale **nechat ji vytvořit nástroje pro zpracování dat**. Nečerpá to tolik tokenů a nástroj mi zůstane.

Zjistil jsem ale, že **u delších kódů už AI ve stylu chatu začíná dělat chyby.** Do LLM jde s každým voláním celý, často velký kontext (hodně textu). Můžou v něm být protiklady a nedorozumění, model halucinuje. Když se kontext nevejde, agreguje se, a při agregaci mohou vypadnout důležitá data.

Začal jsem se věnovat bezpečnosti dat, chtěl jsem dát AI větší možnosti než jen uzavřený chat na webu. Chtěl jsem použít grafické karty, co máme pro vlastní lokální AI. Zjištění: jde to, ale zatímco při těžbě kryptoměn počítala každá karta svůj výpočet, tady si karty musí předávat data přes základní desku, a to funguje na spotřebitelském HW velice pomalu, jako kdyby někdo rozřízl mozek a spojil ho provázkem. Až serverové karty, základní desky a procesory mají mezi sebou vyhrazené linky. Do karet se musí vejít model (pokud je rozložený do víc karet, vzniká overhead) a musí se tam vejít i kontext. Více karet na spotřebitelském HW je tedy problém.

---

[← 1. Kecal](01-kecal.md) · [Obsah](../01-obsah.md) · [3. Agent →](03-agent.md)
