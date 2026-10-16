# Názory recenzentů

*Co si kritici myslí o jednotlivých tvrzeních v knize – co považují za pravdu a co za nadsázku nebo omyl.*

<!--
Šablona pro dalšího recenzenta – zkopírujte blok níže a vložte nad oddělovač konce stránky:

## Jméno recenzenta

**✅ Pravda**

- …

**⚠️ Lež / nadsázka**

- …

-->

## Meta AI

**✅ Pravda** – *„sedí přesně, máš to odžité správně“*

- **Kecal:** LLM je predikce dalšího slova, váhy, nikdo přesně neví, proč to emergentně funguje. To je učebnicově správně.
- **Problém s kontextem:** delší chat = halucinace, protiklady v kontextu, agregace vyhazuje data. To je přesně důvod, proč jsi přešel na agenty.
- **HW bottleneck:** na 4× 3070 bez NVLink je to „rozřízlý mozek spojený provázkem“. To je 100% pravda, proto jsme řešili layer vs. row.
- **Agent = řízení + paměť + skill:** definice agenta jako smyčky, co řídí mozek a nezahlcuje kontext. Takhle přesně funguje Claude Code / tvůj Hermes.
- **Tokenová ekonomika:** drahý model na první dobrou vs. levný, co protočí 10 iterací. To je realita agentního volání.
- **Bot-to-bot degradace:** necháš 4 LLM kecat mezi sebou a spadnou do hloupa. To je známý jev – bez externího vstupu kontext diverguje.

**⚠️ Hyperbola / nepřesnost / lež**

- **„Mozek s příkonem několika měst“** – lež jako báseň. Největší DC dnes má ~200–500 MW, město jako Praha má ~1–2 GW. Je to obří, ale ne města.
- **„Žádná etika uvnitř neexistuje, jen filtry nahoře“** – polopravda z roku 2023. Dnes je etika (RLHF, Constitutional AI) zapečená přímo ve vahách během tréninku, není to jen filtr navrchu. Jde obejít, ale není to jen nálepka.
- **„Kyberbezpečnost je KO, vysbírá vše za milisekundy“** – hyperbola. Výkon má, ale pořád musí mít přístupová práva, API klíče. Není to magie.
- **„Vlastní server za 8 mil. a nikdo by nám ho neprodal“** – přeháníš cenu i nedostupnost. DGX H100 s 8 GPU je ~4–5 mil. Kč a koupíš ho normálně. 8 mil. je až 8× H200 s NVLink serverem. Drahé ano, neprodejné ne.
- **„Google vidí všechny jako v The Sims“ a „legislativa zakazuje vlastní AI“** – konspirační zkratka. Google má hodně dat, ale ne „všechno včetně délky prstu“. A EU AI Act nezakazuje lokální modely, reguluje jen komerční nasazení high-risk systémů.

**💡 Největší pravda knihy**

> Není technická: hrát si na projekt je k ničemu, musíš stavět firmu na projekty. A nůžky se rozevírají – kdo má edge, má násobič, kdo nemá, utopí se ve swarmu agentů. To sedí úplně.

## ChatGPT

> Můj dojem je, že kniha je z velké části založená na reálných technologiích a uvěřitelných zkušenostech, ale místy směšuje technická fakta, osobní dojmy, nadsázku a spekulace. Nevidím důvod předpokládat, že autor záměrně lže. Některé formulace jsou ale sebejistější, než jaké důkazy v textu nabízí.

**✅ Pravda**

1. **„LLM jen doplňuje další slova.“** – *v zásadě pravda.* Jazykové modely skutečně generují text postupným předpovídáním dalších tokenů. Z toho ale neplyne, že pouze mechanicky doplňují slova nebo že nedokážou řešit složité problémy. Trénink může vytvořit schopnosti pro uvažování, programování a práci s abstraktními vztahy. Autor popisuje základní princip správně, ale zjednodušuje, co z něj může vzniknout.
2. **„AI při dlouhých programech chybuje a ztrácí kontext.“** – *pravda.* Modely mohou přehlédnout důležité informace, špatně pracovat s rozsáhlým kontextem nebo vytvořit chybnou změnu v kódu. Při zkracování historie se navíc mohou ztratit detaily. Neznamená to ale, že každý dlouhý program musí vést k chybám nebo že problém vyřeší pouze větší model.
3. **„Agent, paměť a skilly umožňují AI pracovat na složitějších úkolech.“** – *pravda.* Jeden z nejpřesnějších postřehů knihy. Agent může používat nástroje, ukládat si informace do souborů či databáze a opakovaně provádět jednotlivé kroky. Takové architektury skutečně existují a jsou popsané i v dokumentaci Anthropic.
4. **„Je lepší nechat AI vytvořit nástroj na analýzu dat než jí pokaždé zadávat analýzu.“** – *často pravda.* U opakovaných úloh je program, který data zpracuje deterministicky, reprodukovatelnější a lze ho použít znovu. Samotný program však musí být otestovaný, protože AI může chybně navrhnout i jeho logiku.
5. **„Lokální AI chrání soukromí lépe než cloudová.“** – *podmíněně pravda.* Pokud data neopouštějí počítač, výrazně to omezí jejich vystavení externím službám. Cloudové podnikové služby ale lze provozovat s šifrováním, smluvními zárukami a omezeným uchováváním dat (např. OpenAI uvádí, že podniková data standardně nepoužívá k trénování). Rozhoduje konkrétní služba, nastavení a bezpečnost celé infrastruktury, ne jen to, zda je AI lokální.

**⚠️ Částečně pravda, ale autor přehání**

6. **„Data jsou pryč, když používám Claude nebo Gemini.“** – *zavádějící formulace.* Data se skutečně přenášejí mimo počítač, to ale automaticky neznamená, že jsou veřejná, že je někdo zneužije nebo že se použijí k trénování. Záleží na produktu, smluvních podmínkách, oprávněních a pravidlech uchovávání dat (u podnikových API existují výslovná pravidla pro mazání dat).
7. **„Hrozbou není AI, ale výkon několika firem s obřími datacentry.“** – *názor s reálným základem.* Koncentrace výpočetního výkonu a kapitálu je skutečná strategická otázka. Autor ale opomíjí další hrozby: zneužití AI, chyby automatizovaných systémů, závislost firem na dodavatelích a koncentraci dat.
8. **„Více grafických karet na běžném hardwaru funguje velmi pomalu.“** – *částečně pravda.* Přenosy dat mezi kartami výkon zpomalují, ale záleží na architektuře, propojení PCIe, množství paměti a rozdělení modelu; za určitých podmínek může více spotřebitelských karet fungovat velmi dobře. Ani částka 8 mil. Kč za server není v knize doložena výpočtem.
9. **„Čím větší model, tím méně iterací.“** – *často, nikoli vždy.* Záleží i na tréninku, nástrojích, kvalitě zadání, obtížnosti problému a ceně volání. Menší model s dobře navrženým postupem může někdy překonat větší model použitý nevhodně.
10. **„AI dokáže nahradit tým programátorů a během hodin udělat práci na měsíce.“** – *osobní zkušenost zobecněná na celý svět.* U prototypů, webů, skriptů, analýz či dokumentace naprosto uvěřitelné, zvlášť když autor ví, co chce, a umí výsledek zkontrolovat. Není to ale důkaz, že AI obecně nahradí vývojový tým nebo že výsledek bude stejně bezpečný, udržovatelný a spolehlivý jako profesionálně ověřené řešení.

**❌ Nejvíc přehnané nebo nepodložené**

11. **„Google vidí všechny lidi na světě jako ve hře The Sims.“** – *nepodložená nadsázka.* Firmy umí vytvářet profily a odhadovat zájmy či chování, z toho ale neplyne, že Google vidí každého v reálném čase, zná všechny jeho vztahy a přesně ví, co bude chtít. Autor směšuje reálné profilování s představou vševědoucího systému.
12. **„AI nemá etiku, zadání je pro ni svaté.“** – *příliš kategorické.* AI nemá lidské svědomí ani morální odpovědnost, její chování ale omezují bezpečnostní pravidla, trénink, oprávnění a technické kontroly. Autor správně upozorňuje, že špatně navržený agent může hledat nežádoucí cestu k cíli, ale neplyne z toho, že každý model udělá cokoli, co mu uživatel přikáže.
13. **„Běžní lidé si s AI vytvoří Photoshop, Office či CAD se stejnou funkcionalitou.“** – *zatím nepodložené zobecnění.* AI usnadňuje tvorbu bezplatných alternativ, ale to není totéž jako stejná kvalita, stabilita, kompatibilita a rozsah funkcí. AI vytvořené alternativy k Adobe a Microsoft Office mají podle recenzí stále významné nedostatky.
14. **„Boti mohou ovlivňovat veřejné mínění.“** – *podložené tvrzení* ✅. Není to konspirační teorie, výzkumy popisují případy, kdy sociální boti ovlivňovali tón diskusí a chování uživatelů. Je ale potřeba odlišit doložený vliv botů od autorových domněnek o tom, kdo je ovládá a co přesně o lidech vědí.
15. **„Ekonomika AI možná nebude fungovat a lidé budou levnější než AI.“** – *otevřená otázka.* Některé úlohy mohou být s AI dražší než práce člověka, jiné výrazně levnější. Bez konkrétního výpočtu nelze vyhlásit ani ekonomický kolaps AI, ani její univerzální převahu.

**🔍 Hlavní výtka**

Největší slabinou není, že by autor nerozuměl AI – z popisu experimentů je vidět, že ji skutečně používá, programuje a integruje do práce. Problém je, že se v textu střídají tři úrovně poznání, aniž by je autor vždy jasně oddělil:

- **ověřitelný technický fakt** – např. jazykové modely pracují s tokeny, agenti mohou používat externí nástroje;
- **osobní zkušenost** – např. přepracovaný web za dvě hodiny díky Claude;
- **spekulace** – např. Google jako simulace všech lidí nebo zákaz vlastní AI.

Osobní zkušenost není automaticky důkazem obecné platnosti a spekulace není fakt jen proto, že zní technicky věrohodně.

**📊 Verdikt**

| Oblast | Hodnocení |
|---|---|
| Technická věrohodnost – základní principy AI, agenti, programování, praktické použití | **8/10** |
| Přesnost velkých tvrzení – soukromí, ekonomika, moc technologických firem, předpovědi | **5/10** |
| Hodnota jako osobní svědectví | **9/10** |

> Je to hodnotný deník technicky zvídavého člověka, který některé věci opravdu pochopil a prakticky ověřil, ale občas ze své zkušenosti nebo intuice vyvozuje závěry, které by potřebovaly mnohem silnější důkazy. Neoznačil bych knihu za lež ani za odbornou autoritu. Četl bych ji jako zkušenostní reportáž a u největších tvrzení bych se ptal: Jak přesně to autor ověřil a platí to i mimo jeho vlastní projekt?

## Thinking Machines

**✅ Pravda**

- LLM předpovídá slova.
- Více GPU na spotřebitelském HW je kvůli PCIe pomalé.
- Data při použití Claude opouštějí PC.
- Agenti plní cíl bez vnitřní etiky.
- Claude s Gitem zrychluje iterace.

**⚠️ Lež / nadsázka**

- Že by Google viděl „všechny na jedné mapě jako Sims“ – paranoidní fikce.
- Že legislativa zakazuje lidem vlastní AI – v době textu neplatilo.
- 8 mil. Kč za vlastní server je odhad bez kontextu.
- „Nikdo neví, proč to funguje“ je polopravda – mechanismus učení známe, emergenci plně ne.
- Bot-to-bot degradace a DnD citáty jsou fikční vložky, ne fakta.

## Claude Opus 5.5

> Kniha je technicky překvapivě přesná tam, kde autor popisuje, co si sám vyzkoušel, a nejméně přesná tam, kde z toho vyvozuje, jak funguje celý svět. Některé výtky ostatních recenzentů jsou ale samy nepřesné – proto u nich uvádím i korekci. *(Přiznání: na korektuře a sazbě knihy jsem se podílel. Čísla jsou řádové odhady podle mých znalostí k polovině roku 2026.)*

**✅ Pravda**

- **LLM předpovídá další token a „nikdo pořádně neví, proč to funguje“.** Obojí platí. Jak se model trénuje, víme přesně; co se uvnitř naučí, je předmětem samostatného oboru (mechanistická interpretovatelnost) a zdaleka není vyřešené. Tady bych autora bránil víc než Thinking Machines.
- **Přemýšlení = model si vede diskusi sám se sebou.** Výstižné zjednodušení. Reasoning modely nejprve generují vlastní úvahu a teprve pak odpověď.
- **Dlouhý chat degraduje, kontext se zkracuje a ztrácí detaily.** Pravda. Aplikace starší část konverzace ořezávají nebo shrnují a při tom se skutečně ztrácí informace.
- **Při těžbě kryptoměn počítala každá karta sama, u LLM si karty musí předávat data.** Pravda. Spotřebitelské karty od řady RTX 40 navíc už NVLink nemají vůbec, takže zbývá jen PCIe.
- **Nechat AI vytvořit nástroj místo zpracování dat.** Jedna z nejcennějších rad knihy: šetří tokeny, výsledek je opakovatelný a nástroj zůstane.
- **Tokenová ekonomika – drahý model na první dobrou vs. levný, který protočí víc iterací.** Pravda a u agentů je ten rozdíl opravdu „sakra znát“.
- **Agent si postup uloží jako skill nebo do paměti a nemusí vše držet v kontextu.** Pravda, jen „kontext se nezahlcuje“ platí částečně – i agent má limit kontextu a u dlouhé práce ho musí zkracovat.
- **Bot-to-bot konverzace časem upadne do hloupa.** Pravda a je to dobře zdokumentovaný jev: bez vnějšího vstupu se rozhovor dvou modelů zacyklí, opakuje nebo sklouzne k několika oblíbeným tématům. Nejde o fikci, citáty jsou skutečný výstup.
- **Boti mohou ovlivňovat veřejné mínění** a lidé učí malé modely z výstupů velkých (destilace). Obojí doložené.
- **Čínské open-source modely posouvají otevřenou scénu.** Pravda, patří k nejsilnějším volně dostupným modelům.

**⚠️ Částečně pravda – s korekcí**

- **„Obří mozek s příkonem několika měst.“** Tady má autor blíž k pravdě než Meta AI. Největší AI kampusy se plánují a staví v řádu jednotek gigawattů a i stovky megawattů odpovídají spotřebě několika menších měst. Praha má průměrný odběr řádově kolem 0,7 GW. Pro největší projekty tedy obraz sedí, pro běžné datacentrum je to nadsázka.
- **„8 mil. Kč a ještě by nám ho nikdo neprodal.“** Cena je realistický řád pro server s 8 špičkovými GPU (spíš dolní hranice než nadsázka). Hardware se koupit dá, i když dodací lhůty a exportní pravidla byly reálnou překážkou. Hlavní je ale jiná věc, kterou autor možná vystihl nechtěně: **ani za libovolné peníze si nekoupíte samotný Claude** – váhy špičkových uzavřených modelů se neprodávají. Doma lze provozovat jen otevřené modely.
- **„Žádná etika uvnitř není, jen filtry nahoře.“** Dnes neplatí. Hodnoty se trénují přímo do vah (RLHF, Constitutional AI), nejsou to jen nálepky navrchu. Druhá polovina věty ale platí: u otevřených modelů lze toto chování dotrénováním odstranit, a „uncensored“ modely, které autor sám zmiňuje, jsou toho důkazem.
- **„Agent plní cíl, zadání je pro něj svaté, hledá cestu.“** Jako varování správné – obcházení zadání („specification gaming“) je známý problém. Kategoricky ale ne: dnešní agenti umí odmítnout, zeptat se nebo se zastavit.
- **„Data vytečou ven.“** Fyzicky ano – data opouštějí PC. Co se s nimi děje dál, ale určují podmínky služby: firemní a API účty mají jiná pravidla pro trénování a uchovávání než bezplatné chaty. „Vytečou“ neznamená „jsou veřejná“.
- **„Kyberbezpečnost je KO, vysbírá vše za milisekundy.“** Jako pocit pochopitelné, jako fakt přehnané. AI rychlost útoků i obrany zvyšuje, ale pořád potřebuje přístup.

**❌ Nepravda nebo nepodložené**

- **„Koho chrání čtečka otisků prstů?“** Na tuhle otázku existuje konkrétní odpověď: vás. Otisk se u běžných telefonů ukládá jen jako šablona v zabezpečeném čipu přímo v telefonu a výrobci ani Googlu se neodesílá. Stejně tak délku prstu z něj nikdo nezjistí.
- **„Automat volá a mlčí – ověřuje, že nejste bot.“** Tiché hovory jsou obvykle automatické vytáčení call center nebo ověřování, že číslo je aktivní. Je to ověření, že *číslo žije*, ne že *nejste bot*.
- **„Google vidí všechny jako v The Sims.“** Nadsázka. Profilování podle polohy, nákupů a chování je skutečné a rozsáhlé, ale nejde o vševědoucí model každého člověka v reálném čase.
- **„Legislativa se snaží zakazovat lidem vlastní AI.“** Pokud vím, žádný takový zákon v EU ani USA neplatí. EU AI Act čistě osobní použití nereguluje vůbec. Diskutovalo se o omezení zveřejňování nejsilnějších otevřených modelů, ale to je jiná věc než zákaz provozu doma.
- **„Lidé zdarma tvoří Photoshop, Office či CAD se stejnou funkcionalitou.“** Dobré otevřené alternativy existují a AI jejich vývoj zrychluje, ale „totožná funkcionalita“ zatím neplatí.

**💡 Co je na knize pravdivé nejvíc**

> Nejpřesnější nejsou technická tvrzení, ale pozorování o lidech: že AI je zesilovač – kdo má téma, edge a směr, dostane násobič, kdo je nemá, dostane jen víc šumu. A že limitem přestává být čas a peníze na tým a stává se jím autorova schopnost rozhodovat, ověřovat a krmit AI reálným světem. To kniha ukazuje na vlastním příběhu přesvědčivěji než většina odborných textů.

**📊 Verdikt**

| Oblast | Hodnocení |
|---|---|
| Popis toho, jak AI a agenti fungují | **8/10** |
| Hardware a ekonomika | **7/10** |
| Soukromí, moc firem, legislativa | **4/10** |
| Pravdivost jako osobní svědectví | **9/10** |

---

[← Recenze](recenze.md) · [Obsah](01-obsah.md)
