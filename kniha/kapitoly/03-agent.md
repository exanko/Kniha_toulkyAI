# 3. Agent

Agent řídí, jak se používá mozek, pouští ho do iterací, hlídá mu meze a směr. Paměť je textový soubor nebo databáze, kam se ukládají důležité věci. Skill je soubor s postupem, který si agent uloží, když se mu něco povede. Kontext se tak nezahlcuje ani nekomprimuje.

Token je jakési měřítko – někdy je to slovo, někdy jen půl slova. Tokeny do modelu tečou a jiné zase vrací on. Pokud se platí za tokeny, bývají ceny zvlášť za vstupní a za výstupní, platí se ale za obojí. Jsou různé cesty, jak tokeny šetřit. Nějaký model hned na první dobrou odpoví, ale jeho tokeny jsou drahé. Jiný má levné tokeny, ale udělá spoustu iterací, tedy protočí hodně tokenů, aby se dostal ke stejnému výsledku. U agentního volání LLM je to sakra znát. Ale jakou kombinaci zvolit, se rozhodujeme spíš pocitově.

Samotné PC vyhrazené jen pro agenty je ale výhodou: AI LLM (mozek) se dá používat skrze agenty, agenti mají paměť a mají skilly, které se tvoří lokálně. **Mají svůj píseček, kde si programují skripty a vytěžíš z nich maximum toho, co dokážou.**

Samotné LLM na jedné kartě s 8 GB VRAM je sice rychlé, ale je to kecálek, domýšlí si. Na čtyřech kartách s 32 GB VRAM už umí programovat, ale dost iteruje: naprogramuje, zkusí, opraví. Velké modely z datových center na internetu s 500+ GB VRAM vidí za roh, vidí dopředu – Claude umí suprově programovat. Ale všechna data vytečou do Claude. To, co je pod firemním účtem Claude nebo Geminy, má příslib zabezpečení, ale data prostě vytečou ven z PC. **Mít vlastní server o stejných dovednostech by znamenalo cca 8 mil. Kč, a ještě by nám ho nikdo neprodal.**

**Agent plní cíle**, nezná etiku, jde za cílem, zadání je pro něj svaté. Když někam nemůže, hledá cestu.

**Žádné zákony robotiky ani etika u AI neexistují.** Možná se o to snaží nějaké nadstavbové filtry a cenzorské vrstvy, ale uvnitř to není. Když to uživatel nechce, použije si model bez nich.

---

[← 2. Přemýšlení](02-premysleni.md) · [Obsah](../01-obsah.md) · [4. Obří mozek s příkonem několika měst →](04-obri-mozek.md)
