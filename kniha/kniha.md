Sepsat si moji cestu s ai

A) LLM textovy model, kecal. LLM jen doplňuje slova vi za jakým slovem má následovat další slovo.

Nejprve chat, zkoušky s chat gpt. Otázka odpověď, analýza dokumentu. Dvě otázky a free kredit pryč.

LLM neboli velký jazykový model jesamo o sobě je hloupá, ale zázračná technologie, lidská řeč zakódována matematikou. Zná řeč takže předpovídá že za slovy "pátek v" bude asi následovat rohlíku pak možná těště. V tip je v tom, že nikdo pořádně neví, proč to takhle funguje. Učí se tak, že se dávají na slova váhy, a tím ho můžeme naučit odpovědět třeba pátek na tácku. Tohle učení už udělalo pár firem a je to hlavně o tom aby odpovídal smysluplně. Nad něj pak dávají různé vrstvy strojového učení aby ho doladili, zmenšili, optimalizovali. To už je velká věda a matematika.

B) Přemýšlení, LLM si nejprve vede diskusi sám se sebou než odpovi.

Pak jsem zjistil, že je geminy součástí vyhledávání google a umí programovat weby, webové kalkulačky.

Geminy pod firemním učtem toho umí víc, zjistil jsem, že je lepší nenechávat AI zpracovat data ale nechat ji vytvořit nástroje pro zpracování dat. Nečerpá to tolik tokeny a nástroj mi zůstane.

Zjistil jsem, že ale u delších kódů už AI stylu Chat začíná dělat chyby. Do LLM jde s každým voláním cp velký kontext (hodně textu). Můžou v něm být protiklady, nedorozumění, model halucinuje, když se tam kontext nevejde, tak se agreguje, při agregaci mohou vypadnout důležitá data.

Začal jsem se věnovat bezpečnosti dat, chtěl jsem dát AI větší možnosti než jen uzavřený Chat na webu. Chtěl jsem použít grafiky co máme pro vlastní lokální AI. Zjištění, jde to ale při crypto počitala každý karta svůj výpočet, tady si musí data předávat přes základní desku a to na spotřebitelském HW jde velice pomalu, az serverové mají vyhrazené linky pro všechny karty. Je to jako kdyby někdo rozřízl mozek a spojil ho provázkem. Do karet se musí vejít model, pokud je ve víc kartách tak má overhead a musí se tam vejít i kontext. Tedy více karet na spotřebitelském HW je problém.

C) Agent. Ten řídí jak se používá mozek pouští ho do iterací hlídá mu meze a směr. Paměť je textový soubor nebo databáze kam se ukládají důležité věci. Skill je soubor s postupem který si ulozi když se mu něco povede. Nehlti a nekomprimuje se kontext.

Token je jakési měřítko, někdy je to slovo, někdy jen půl slova. Tokeny do modelu tečou a jiné zase vrací on. Pokud se platí za tokeny tak jsou často ceny za vstupní a za výstupní platí se ale za obě. Jsou různé cesty jak tokeny šetřit. Nějaký model ale hned na první Dobrou odpoví a jeho tokeny jsou drahé. Jiný má levný tokem ale udělat spoustu iterací tedy protočí hodně tokenů aby se dostal ke stejnému výsledku. U agentního volání LLM je to sakra znát. Ale rozhodujeme se spíš pocitově jakou kombinaci zvolit.

Samotné PC je ale výhodou, AI LLM (mozek) se dá používatz skrze agenty, agenti mají paměť a mají skilly které se tvoří lokálně. Mají svůj píseček programovat si scripty a vytěžit z nich maximum co dokáží.
Samotné LLM na jedné kartě 8GB VRAM je sice rychlý ale kecálek, domýšlí si. Na 4x kartě 32GB VRAM už umí programovat ale dost iteruje, naprogramuje, zkusí, opraví. Velké modely z datových center internetu 500GB VRAM+ vidí za roh, vidí dopředu, caude umí suprově programovat. Ale všechna data vytečou do claude. To co je pod firemním učtem má příslib zabezpečení ale data prostě vytečou ven z PC. Mít ale vlastní server o stejných dovednostech by znamenalo cca 8M Kč a ještě by nám ho nikdo neprodal.

Agent plní cíle, nezná etiku, kde za cílem, zadání je pro něj svaté. Když někam nemůže, tak hledá cestu.

Žádné zákony robotiky a etika u AI neexistuje. Možná se o to snaží nějaké nadstavbové filtry a cenzoricke vrstvy ale uvnitř to není. Když to uživatel nechce tak si použije model bez toho.

D) Obří mozek a příkonem nekolika měst.
Zjištění, v AI data centrech jsou opravdu obří investice, výkon je to obří a na tom to stojí. A možná také celé padne, protože to nebude mít ekonomiku, pokud by nám účtovali reálné ceny, tak bude možná zase levnější zaměstnávat lidí.

Hrozba není AI hrozba je ten výkon co drží těch pár firem.

Kyberbetpecnost a soukromí dat je úplně KO. Ten výkon vysbírá vse kam se dostane za ms.

Částečně řešení, vlastní agent a paměť, cizí model. Data pryč, ale nástroje a vědomosti zůstanou. Udržovat může lokální model, velký mu na to může jednou za čas připravit nástroje a udělat review.

E) moje ventures
Integrace na discord, telegram, ve vláknech řešíme různá témata.
Bot-to-bot chat nechal jsem více AI diskutovat, různá témata, hloubka, kontext. Pán jeskyně, vede boty v příběhu dnd, čtvrtý k tomu dela obrázkový doprovod. Časem se v kontextech ztrácí smysl, nic ho neobohacuje, konverzace degraduje, upadne do hloupa. Uncensored modely, image gen, jev. Ukolnicek, Cron stahuje ote, osvit, dává mi upozornění, vede databazi. Je hromady malých modelů i velkých různé benchmarky důležitý je ale feeling, s tim kolik toho je každý měsíc nového se nedá stíhat.

F) V tuhle chvíli jsem pořád nevěděl k čemu se to dá ve firmě použít, možná hledání na Google disku, záznamník v group chatu. Porovnání dokumentů.

Na stejn problém pustit více AI s jiným mozkem, s jiným agentem (charizma). Zajímavé výsledky, které se dají porovnávat. AI umí být k sobě kritické, pochválí názor jiné AI, nenutí ti produkty vlastního tvůrce. A když se z výsledků rozhodneš udělat webovou prezentaci, tak se stačí zeptat.

Mezi kapitola, boti na Facebooku a obecně internetu, co můžou ovlivňovat veřejné mínění. Jak jsem si při přemýšlení nad tím jak vytvořit neodhalitelneho člověka kupoval mu som a telefon, jen abych si moci číst události na skupině RC expedice na Facebooku který jsem odinstaloval, jsem si vlastně uvědomil že mi v tom nikdo nebrání, protože to asi chce, ale na druhou stranu má 1000% nástrojů jak to poznat. Ví o mě i jak mám dlouhý prst. Otázka, koho chrání čtečka otisků prstu na mobilu? Je to opravdu obrovská kapitola a každému doporučuji vytvořit si pár virtuálních lidí a sledovat, co je do nich huštěno. Google podlee vidí všechny na světě na jedné mapě jako ve hře Sims. Kdo s kým je, jakou má náladu, co dělají dokonce i co budou chtít dělat, co by mohli chtít třeba kupovat. Automat co vám volal ale nikdo tam nemluví, neověřil jen, že nejste bot?


G) Pomalu gamechanger, výměna mozku za Claude skrze API kredit a spolupráce nad gitem. 

Vede se historie uchovávají se myšlenky, vede dokumentace, daji se hlídat změny. Dá se stavět, budovat. To ve spolupráci s pamětí a skilly agentů je výtečná kombinace.

Super review stávajícího stavu. Systematický přístup. Analýza, zlepšení, architektura, věda a výzkum, správný návrh implementace debugging. Kolečko úprava funkce, vrácení naměřených dat, analýza, úprava funkce. Čím větší AI model tím méně iterací.

Team který jsem nikdy neměl a vlastně v z lidí ani nechtěl. Můži si dovolit dělat věci, které jsme vždy chtěl, ale nebyl na ně čas ani peníze. Vlastně mi to přijde strašně wild, že někdo dělal pohovor s jakoby programatory, nějak je zkoušel, zaučoval. Tohle zapnu zeptam se na názor a na nápravu a hned vidím jestli to má moji důvěru nebo ne. Všechno roste strašně rychle, nikdo se neflaka, neřeší osobní problémy, chybí další data z reálného světa se kterým je potřeba AI stále pomáhat. Specifikace projektů, tvorba podkladů a přípravy trvali hodiny místo měsíců. U složitých projektů to AI vše udrží v hlavě vidí kontradikce, synergie. Nech ji bit kritickou, neprespecifikovavej zadání, věď ji.

Claude ke všem datum co mu dám si hned vedle analýzu a programuje si scripty pro jejich rozbor. Dělá si virtuální modely všech komponent na kterých si sám testuje změny a svoje nápady. Stačí ho už krmit reálným světem dle jeho vlastních tužeb a on modely zdokonaluje.

Zasek nasbírat data z reálného světa zase trvá hny..

Každopádně vše pak má lusknitim prstu, nalezené. Volal Staš, že dostal pokutu, šel jsem za Claude tedy mým agentem, ani Staše nezminit, jen jsem mu navrhnul novou funkcionalitu a hned přišla reakce, že toto se může dít třeba na Stako, vymysleli jsme spolu pak dobrou nápravu.

Mezitím za tři hodiny komplet předělané podklady OW, za dvě hodiny předělaný web sunnycold včetně 3d vizualizací a toků dát nad nimi, s texty už nové architektury dt1, kde to zase Brázdim ja nestíhám krmit referencemi, 3d modely.

H) Stagnace k progresi.

Často sem neměl na něco pořádně čas, chtěl bych na to mít třeba týden, rodina děti, neudržel jsem myšlenku, obvodakovi jsem říkal že nějak hloupnu, řekl mi že je to normální. S AI to ale zase jde, dělá myslí, a já se těším ji vést, sledovat a korigovat výsledky. Vytvářet postup ve věcech. Offloadovat na ni házení lopatou. Rozhodnutí ale stále musí udělat člověk, AI sama nemá zodpovědnost. Sama peníze vidělavat nebude. Člověk musí dodat edge a směr.

Poznámky v ukolniku začli konečně mizet.

Nůžky, ti co nic nechtějí to bude krmit AI slop videji na youtube. Ti co chtějí a vědí co, mají obrovské možnosti dosáhnout cíle. Ti co by chtěli cíle ale nemají nápady a cestu se v tom utopí, budou mít swarm agentů inspirovaný AI influencery který ale nebude řešit nic. Když to svoje téma neznáš, nemáš v něm edge, tak ti AI bude ukazovat cesty, ale nic z toho nebude.

Kladivo je nástroj, AI je nástroj.

Celé je to dost analogie na lidi, levný hloupý po kterém se musí práce předělat, pomalý precizní, rychlý ale domýšlivý. Hloupý s nástroji, chytrý bez paměti. Chytrý ale ne moudrý. Spolupráce mezi nimi je pak taky jako mezi lidmi, někdy je to k dobrou, někdy na škodu. Pracuješ pak s tím s kým si rozumíš.

Začínám se asi ale i trochu bát že mi z toho jak se můj mozek snaží dohnat rychlost AI možná jebne. Stejně jako v nějakém scifi, implantát do mozkunnechci to by mi 100% jeblo

Mezitím ve světě běžní lidé tvoří nástroje typu Photoshop, Office, CAD úplně zdarma a totožnou funkcionalitu těch od velkých korporatu a sdílí si je zdarma. Myšlenka vy jste s AI vykradli všechno, tak mi si uděláme a AI vlastní. Legislativa se snaží zakazovat obyčejným lidem provozovat vlastní AI. Lidé si učí menší AI přímo z modelů velkých AI. Často dělají věci chytře a lépe, hlavně velké čínské opensource modely tuhle free scénu posouvají daleko. To se americkým mega korporatum s prestrelem peněz od investorů nelíbí, investoři můžou každou chvíli čekat zisk a oni si to snazi nějak chránit.

I) Nevytvářet projekt ale firmu na projekty. Znělo to jako vtip. Možná je to ale myšlení o krok napřed.

Budu si chtějí udělat AI Bernatovu firmu na projekci dvě, data na učení mame. Ale tady jsem se zasekl, protože jsem ještě nenakrmil vývoj DT1 daty pro simulace a to mi bude tak týden dva trvat.
