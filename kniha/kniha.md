Sepsat si moji cestu s AI

A) LLM – textový model, kecal. LLM jen doplňuje slova – ví, za jakým slovem má následovat další slovo.

Nejprve chat, zkoušky s ChatGPT. Otázka – odpověď, analýza dokumentu. Dvě otázky a free kredit pryč.

LLM neboli velký jazykový model je sám o sobě hloupá, ale zázračná technologie – lidská řeč zakódovaná matematikou. Zná řeč, takže předpovídá, že za slovy „párek v“ bude asi následovat „rohlíku“, pak možná „těstě“. Vtip je v tom, že nikdo pořádně neví, proč to takhle funguje. Učí se tak, že se slovům dávají váhy, a tím ho můžeme naučit odpovědět třeba „párek na tácku“. Tohle učení už udělalo pár firem a jde hlavně o to, aby odpovídal smysluplně. Nad něj pak dávají různé vrstvy strojového učení, aby ho doladili, zmenšili, optimalizovali. To už je velká věda a matematika.

B) Přemýšlení – LLM si nejprve vede diskusi sám se sebou, než odpoví.

Pak jsem zjistil, že Gemini je součástí vyhledávání Google a umí programovat weby a webové kalkulačky.

Gemini pod firemním účtem toho umí víc. Zjistil jsem, že je lepší nenechávat AI zpracovávat data, ale nechat ji vytvořit nástroje pro zpracování dat. Nečerpá to tolik tokenů a nástroj mi zůstane.

Zjistil jsem ale, že u delších kódů už AI ve stylu chatu začíná dělat chyby. Do LLM jde s každým voláním celý, často velký kontext (hodně textu). Můžou v něm být protiklady a nedorozumění, model halucinuje. Když se kontext nevejde, agreguje se, a při agregaci mohou vypadnout důležitá data.

Začal jsem se věnovat bezpečnosti dat, chtěl jsem dát AI větší možnosti než jen uzavřený chat na webu. Chtěl jsem použít grafické karty, co máme, pro vlastní lokální AI. Zjištění: jde to, ale zatímco při těžbě kryptoměn počítala každá karta svůj výpočet, tady si karty musí předávat data přes základní desku, a to jde na spotřebitelském HW velice pomalu – až serverové karty mají mezi sebou vyhrazené linky. Je to, jako kdyby někdo rozřízl mozek a spojil ho provázkem. Do karet se musí vejít model (pokud je rozložený do víc karet, vzniká overhead) a musí se tam vejít i kontext. Více karet na spotřebitelském HW je tedy problém.

C) Agent. Ten řídí, jak se používá mozek, pouští ho do iterací, hlídá mu meze a směr. Paměť je textový soubor nebo databáze, kam se ukládají důležité věci. Skill je soubor s postupem, který si agent uloží, když se mu něco povede. Kontext se tak nezahlcuje ani nekomprimuje.

Token je jakési měřítko – někdy je to slovo, někdy jen půl slova. Tokeny do modelu tečou a jiné zase vrací on. Pokud se platí za tokeny, bývají ceny zvlášť za vstupní a za výstupní, platí se ale za obojí. Jsou různé cesty, jak tokeny šetřit. Nějaký model hned na první dobrou odpoví, ale jeho tokeny jsou drahé. Jiný má levné tokeny, ale udělá spoustu iterací, tedy protočí hodně tokenů, aby se dostal ke stejnému výsledku. U agentního volání LLM je to sakra znát. Ale jakou kombinaci zvolit, se rozhodujeme spíš pocitově.

Samotné PC je ale výhodou: AI LLM (mozek) se dá používat skrze agenty, agenti mají paměť a mají skilly, které se tvoří lokálně. Mají svůj píseček, kde si programují skripty a vytěží z nich maximum, co dokážou.
Samotné LLM na jedné kartě s 8 GB VRAM je sice rychlé, ale je to kecálek, domýšlí si. Na čtyřech kartách s 32 GB VRAM už umí programovat, ale dost iteruje: naprogramuje, zkusí, opraví. Velké modely z datových center na internetu s 500+ GB VRAM vidí za roh, vidí dopředu – Claude umí suprově programovat. Ale všechna data vytečou do Claude. To, co je pod firemním účtem, má příslib zabezpečení, ale data prostě vytečou ven z PC. Mít vlastní server o stejných dovednostech by znamenalo cca 8 mil. Kč, a ještě by nám ho nikdo neprodal.

Agent plní cíle, nezná etiku, jde za cílem, zadání je pro něj svaté. Když někam nemůže, hledá cestu.

Žádné zákony robotiky ani etika u AI neexistují. Možná se o to snaží nějaké nadstavbové filtry a cenzorské vrstvy, ale uvnitř to není. Když to uživatel nechce, použije si model bez nich.

D) Obří mozek s příkonem několika měst.
Zjištění: v AI datových centrech jsou opravdu obří investice, výkon je obří a na tom to celé stojí. A možná to také celé padne, protože to nebude mít ekonomiku – pokud by nám účtovali reálné ceny, bude možná zase levnější zaměstnávat lidi.

Hrozbou není AI, hrozbou je ten výkon, který drží těch pár firem.

Kyberbezpečnost a soukromí dat jsou úplně KO. Ten výkon vysbírá všechno, kam se dostane, za milisekundy.

Částečné řešení: vlastní agent a paměť, cizí model. Data jsou pryč, ale nástroje a vědomosti zůstanou. Udržovat je může lokální model, velký mu na to může jednou za čas připravit nástroje a udělat review.

E) Moje ventures
Integrace na Discord a Telegram, ve vláknech řešíme různá témata.
Bot-to-bot chat: nechal jsem více AI diskutovat – různá témata, hloubka, kontext. Pán jeskyně vede boty v příběhu DnD, čtvrtý k tomu dělá obrázkový doprovod. Časem se v kontextech ztrácí smysl, nic ho neobohacuje, konverzace degraduje, upadne do hloupa. Uncensored modely, image gen, jev. Úkolníček: cron stahuje OTE a osvit, dává mi upozornění, vede databázi. Je hromada malých i velkých modelů a různých benchmarků, důležitý je ale feeling. S tím, kolik toho je každý měsíc nového, se to nedá stíhat.

F) V tuhle chvíli jsem pořád nevěděl, k čemu se to dá ve firmě použít. Možná hledání na Google Disku, záznamník v group chatu, porovnání dokumentů.

Na stejný problém pustit více AI s jiným mozkem, s jiným agentem (charisma). Zajímavé výsledky, které se dají porovnávat. AI umí být k sobě kritická, pochválí názor jiné AI, nenutí ti produkty vlastního tvůrce. A když se z výsledků rozhodneš udělat webovou prezentaci, stačí se zeptat.

Mezikapitola: boti na Facebooku a obecně na internetu, kteří můžou ovlivňovat veřejné mínění. Když jsem přemýšlel, jak vytvořit neodhalitelného člověka, a kupoval mu SIM a telefon, jen abych si mohl číst události ve skupině RC expedice na Facebooku, který jsem odinstaloval, uvědomil jsem si, že mi v tom nikdo nebrání, protože to asi chce – ale na druhou stranu má 1000 % nástrojů, jak to poznat. Ví o mně i to, jak dlouhý mám prst. Otázka: koho chrání čtečka otisků prstů na mobilu? Je to opravdu obrovská kapitola a každému doporučuji vytvořit si pár virtuálních lidí a sledovat, co je do nich hustěno. Google podle mě vidí všechny na světě na jedné mapě jako ve hře The Sims. Kdo je s kým, jakou má náladu, co dělá, dokonce i co bude chtít dělat, co by mohl chtít třeba kupovat. Automat, co vám volal, ale nikdo tam nemluvil – neověřoval jen, že nejste bot?


G) Pomalu gamechanger: výměna mozku za Claude skrze API kredit a spolupráce nad Gitem.

Vede se historie, uchovávají se myšlenky, vede se dokumentace, dají se hlídat změny. Dá se stavět, budovat. To je ve spolupráci s pamětí a skilly agentů výtečná kombinace.

Super review stávajícího stavu. Systematický přístup. Analýza, zlepšení, architektura, věda a výzkum, správný návrh implementace, debugging. Kolečko: úprava funkce, vrácení naměřených dat, analýza, úprava funkce. Čím větší AI model, tím méně iterací.

Tým, který jsem nikdy neměl a vlastně ho z lidí ani nechtěl. Můžu si dovolit dělat věci, které jsem vždy chtěl, ale nebyl na ně čas ani peníze. Vlastně mi přijde strašně wild, že někdo dělal pohovory s programátory, nějak je zkoušel, zaučoval. Tohle zapnu, zeptám se na názor a na nápravu a hned vidím, jestli to má moji důvěru, nebo ne. Všechno roste strašně rychle, nikdo se neflaká, neřeší osobní problémy – chybí jen další data z reálného světa, se kterými je potřeba AI stále pomáhat. Specifikace projektů, tvorba podkladů a příprav trvaly hodiny místo měsíců. U složitých projektů to AI všechno udrží v hlavě, vidí kontradikce i synergie. Nech ji být kritickou, nepřespecifikovávej zadání, veď ji.

Claude si ke všem datům, co mu dám, hned vede analýzu a programuje si skripty pro jejich rozbor. Dělá si virtuální modely všech komponent, na kterých si sám testuje změny a svoje nápady. Stačí ho už jen krmit reálným světem podle jeho vlastních tužeb a on modely zdokonaluje.

Zásek: nasbírat data z reálného světa zase trvá dny.

Každopádně všechno pak mám lusknutím prstu nalezené. Volal Staš, že dostal pokutu. Šel jsem za Claudem, tedy za svým agentem, Staše jsem ani nezmínil, jen jsem mu navrhnul novou funkcionalitu – a hned přišla reakce, že tohle se může dít třeba na Stako. Vymysleli jsme pak spolu dobrou nápravu.

Mezitím za tři hodiny kompletně předělané podklady OW, za dvě hodiny předělaný web sunnycold včetně 3D vizualizací a toků dat nad nimi, s texty už nové architektury DT1, kde to zase brázdím já a nestíhám to krmit referencemi a 3D modely.

H) Od stagnace k progresi.

Často jsem na něco neměl pořádně čas, chtěl bych na to mít třeba týden – rodina, děti, neudržel jsem myšlenku. Obvoďákovi jsem říkal, že nějak hloupnu, a on mi řekl, že je to normální. S AI to ale zase jde: dělá, myslí a já se těším, že ji budu vést, sledovat a korigovat výsledky. Vytvářet ve věcech postup. Offloadovat na ni házení lopatou. Rozhodnutí ale stále musí udělat člověk, AI sama nemá zodpovědnost. Sama peníze vydělávat nebude. Člověk musí dodat edge a směr.

Poznámky v úkolníčku začaly konečně mizet.

Nůžky: ty, kdo nic nechtějí, bude krmit AI slop videi na YouTube. Ti, kdo chtějí a vědí co, mají obrovské možnosti dosáhnout cíle. Ti, kdo by chtěli cíle, ale nemají nápady a cestu, se v tom utopí – budou mít swarm agentů inspirovaný AI influencery, který ale nebude řešit nic. Když svoje téma neznáš, nemáš v něm edge, tak ti AI bude ukazovat cesty, ale nic z toho nebude.

Kladivo je nástroj, AI je nástroj.

Celé je to dost analogie na lidi: levný hloupý, po kterém se musí práce předělat; pomalý precizní; rychlý, ale domýšlivý. Hloupý s nástroji, chytrý bez paměti. Chytrý, ale ne moudrý. Spolupráce mezi nimi je pak taky jako mezi lidmi – někdy je to k dobrému, někdy na škodu. Pracuješ pak s tím, s kým si rozumíš.

Začínám se ale asi i trochu bát, že mi z toho, jak se můj mozek snaží dohnat rychlost AI, možná jebne. Stejně jako v nějakém sci-fi – implantát do mozku nechci, to by mi stoprocentně jeblo.

Mezitím ve světě běžní lidé tvoří nástroje typu Photoshop, Office či CAD úplně zdarma, s totožnou funkcionalitou jako ty od velkých korporátů, a sdílejí si je zdarma. Myšlenka: vy jste s AI vykradli všechno, tak my si s AI uděláme vlastní. Legislativa se snaží zakazovat obyčejným lidem provozovat vlastní AI. Lidé si učí menší AI přímo z modelů velkých AI. Často dělají věci chytře a lépe, hlavně velké čínské open-source modely tuhle free scénu posouvají daleko. To se americkým megakorporacím s přestřelem peněz od investorů nelíbí – investoři můžou každou chvíli čekat zisk, a tak se to snaží nějak chránit.

I) Nevytvářet projekt, ale firmu na projekty. Znělo to jako vtip. Možná je to ale myšlení o krok napřed.

Budu si chtít udělat AI Bernatovu firmu na projekci dvě, data na učení máme. Ale tady jsem se zasekl, protože jsem ještě nenakrmil vývoj DT1 daty pro simulace, a to mi bude tak týden dva trvat.
