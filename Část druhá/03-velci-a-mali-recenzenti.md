# Závěr: Velcí a malí recenzenti

*Analýza recenzí Části druhé. Napsal Claude Opus 5.5 na přání autora.*

V Části první autor napsal:

> Samotné LLM na jedné kartě s 8 GB VRAM je sice rychlé, ale je to kecálek, domýšlí si. Na čtyřech kartách s 32 GB VRAM už umí programovat, ale dost iteruje. Velké modely z datových center vidí za roh, vidí dopředu.

Část druhou pak hodnotilo dvanáct AI recenzentů – od cloudových modelů z datových center až po malé modely, které běží na jedné domácí kartě. Nevědomky tak vznikl experiment, který tuto větu ověřuje. Tady je jeho výsledek.

## Kdo co četl

| Recenzent | Velikost | Hodnocení | Zmínil workflow | Našel slabinu |
|---|---|---|---|---|
| Meta AI | cloud | 8,5 | ✅ | ✅ |
| Gemini | cloud | 8 | ✅ | ✅ |
| ChatGPT | cloud | 8,2 | ✅ | ✅ |
| Claude Opus 5.5 | cloud | 7,5 | ✅ | ✅ |
| Qwen 3.7 Plus | cloud | 8 | ✅ | ✅ |
| Nemotron 3 Ultra | cloud | 9 | ✅ | ❌ |
| Inkling | cloud | 7 | ✅ | ✅ |
| Qwen 3.8 27B | 27 mld. parametrů | 7 | ✅ | ✅ |
| Bonsai 2 27B | 27 mld. parametrů | 8 | ❌ | ✅ |
| Qwen3 8B | 8 mld. parametrů | 8 | ❌ | jen „obtížné pro široké publikum“ |
| Qwen 3.5 4B uncensored | 4 mld. parametrů | 8 | ❌ | ❌ |
| Qwen 3.5 0.8B | 0,8 mld. parametrů | 9 | ❌ | ❌ |

## Co ukázal experiment

**1. Malé modely čtou jen to, co je hlasité.** Žádný model pod 27 miliard parametrů nezmínil workflow, normy ani jedinou autorovu kapitolu. Všechny popsaly jen filozofický dialog – nejdelší a nejvýraznější část textu. Kniha se pro ně zúžila na rozhovor s Meta AI.

**2. Malé modely si domýšlejí.** Qwen 3.5 4B píše, že „autor tvrdí, že všechno, co člověk vytvořil, je jen objev“. Autor to netvrdil – ptal se. Tvrdila to Meta AI. Qwen 0.8B označil rekurzi za „závěrečnou část“, ačkoli je uprostřed knihy. Přesně to je kecálek z Části první: plynulá, sebejistá věta, která se s textem úplně nepotkala.

**3. Čím menší model, tím vyšší známka.** Nejmenší recenzent (0,8 mld.) dal 9/10 a nenašel jedinou výtku. Velké modely dávaly nižší známky a pojmenovaly konkrétní slabiny – nevyváženost, krátké kapitoly, spekulace podané jako fakta. Malý model chválí, protože neumí kritizovat; velký kritizuje, protože text skutečně přečetl.

**4. Hranice leží zhruba tam, kde ji autor odhadl.** Modely kolem 27 miliard parametrů – zhruba to, co se vejde do 32 GB VRAM – jsou přechod. Qwen 3.8 27B už zmínil workflow i normy a našel strukturální slabiny. Bonsai 2 27B workflow nezmínil, ale jako jediný menší model zachytil podstatu knihy (AI jako zesilovač, ne hrdina) a všiml si, že text „závisí na autoritě rozhovoru s AI“. Modely pod touto hranicí už jen převyprávěly nejhlasitější kapitolu.

## Co je na tom zajímavější než velikost

I velcí recenzenti mají společnou slepou skvrnu: **všech dvanáct označilo za nejsilnější část filozofický dialog**, a ne autorovu zkušenost s technologií. Workflow, normy, „devět matek“, IP adresy agenta nebo „práce je hra“ hodnotili jen okrajově, nebo vůbec.

Důvod je možná prostý. Jazykový model umí posoudit text o myšlení, protože je sám z textu. Zda workflow s Gitem opravdu funguje, se ale z textu posoudit nedá – to se ověří jen tím, že ho někdo použije. Recenzenti tak chválí to, co umí přečíst, a přeskakují to, co by museli vyzkoušet.

**Část druhá se jmenuje „AI je zesilovač“ – a recenze jsou toho důkazem.** Každý recenzent zesílil to, co v knize uměl vidět. Malý model zesílil nejhlasitější kapitolu. Velký model zesílil strukturu a slabiny. Žádný z nich nezesílil to, co by vyžadovalo zkušenost mimo text. Tu musí dodat člověk.

---

[← Recenze](02-recenze.md) · [Obsah](01-obsah.md) · [Diskuse s autorem →](04-diskuse.md)
