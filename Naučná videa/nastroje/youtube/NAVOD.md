# Nahrávání na YouTube přes GitHub Actions

Workflow **„Nahrát na YouTube“** nahraje jazykové verze dílu podle souboru `Naučná videa/<díl>/youtube.json` (název, popis, štítky, soubor), zařadí je do playlistu jazyka (`kanal.json`) a ID videa zapíše zpátky do repa.

**Spouští se samo po sloučení do `main`** (když se změní některý `youtube.json` nebo `kanal.json`) **a jednou denně** v 10:17 UTC, kdy už je obnovená denní kvóta YouTube API. Pokaždé nahraje všechno, co ještě nemá `videoId`, a **naplánuje zveřejnění** – v každém jazyce jedno video denně (od zítřka, nebo den po posledním naplánovaném), v čase z `kanal.json`: CZ 18:00 Praha, EN 12:00 New York, ES 18:00 Ciudad de México, HI 18:00 Indie, PT 18:00 São Paulo. Konkrétní termín jde předepsat v `youtube.json` (`"zverejneni": "2026-12-01T18:00"`). Do té doby jsou videa soukromá a v YouTube Studiu je vidíte jako naplánovaná. Zároveň udržuje playlisty (viz [Playlisty](#playlisty)); denní běh tak dodělá, co předchozí běh nestihl.

Co zůstává ruční (YouTube to přes API nedovolí): **související video** u Shortu a **vlastní miniatura** u Shortu.

## Jednorázové nastavení (asi 15 minut)

**Nahrávání potřebuje vlastní projekt v Google Cloud.** Denní kvóta YouTube API (10 000 jednotek) patří projektu, ne kanálu – kdyby projekt sdílel jiný nástroj (např. služba pro livestream, která si čte chat), spotřebuje kvótu sám a na playlisty nezbude (tak se to stalo v listopadu 2026).

### 0. Nový projekt a YouTube Data API

1. Google Cloud Console (https://console.cloud.google.com) → výběr projektu nahoře → **New project** → název např. `Naucna videa` → Create a přepnout se do něj.
2. **APIs & Services → Library** → vyhledat **YouTube Data API v3** → **Enable**.

### 1. Přihlašovací obrazovka a stav „In production“

Google Cloud Console → **Google Auth Platform** (dříve „OAuth consent screen“). V novém projektu nejdřív **Get started**: název aplikace (např. `Naucna videa – nahravani`), e-mail podpory, Audience **External**, kontaktní e-mail → Create. Pak **Audience**:

- Pokud je **Publishing status: Testing**, klikněte na **Publish app**. V režimu Testing přihlášení po 7 dnech vyprší a nahrávání by přestalo fungovat.
- Ověřování aplikace u Googlu není potřeba – pro vlastní účet stačí, že se při přihlášení jednou odklikne varování „Google tuto aplikaci neověřil“.

### 2. Nový OAuth klient jen pro nahrávání

**Google Auth Platform → Clients → Create client** (dříve Credentials → Create credentials → OAuth client ID):

- **Application type:** Web application
- **Name:** např. `GitHub Actions – nahrávání`
- **Authorized redirect URIs:** `https://developers.google.com/oauthplayground`

Po vytvoření si zkopírujte **Client ID** a **Client secret**. (Služba pro streamování zůstane ve svém původním projektu – každý projekt má svou kvótu.)

### 3. Obnovovací token (refresh token) přes OAuth Playground

1. Otevřete https://developers.google.com/oauthplayground
2. Vpravo nahoře ozubené kolo (OAuth 2.0 configuration): zaškrtněte **Use your own OAuth credentials**, vložte Client ID a Client secret z kroku 2, **Access type: Offline**. Zavřete.
3. Vlevo do pole „Input your own scopes“ vložte `https://www.googleapis.com/auth/youtube` a klikněte **Authorize APIs**.
4. Přihlaste se účtem, kterému patří kanál (u kanálu pod značkovým účtem vyberte kanál). U varování „Google tuto aplikaci neověřil“ → **Rozšířené → Přejít na…** → **Povolit**.
5. **Step 2 → Exchange authorization code for tokens** → zkopírujte **Refresh token**.

### 4. Tajemství v GitHubu

Repozitář na GitHubu → **Settings → Secrets and variables → Actions** → u existujícího tajemství tužka (**Update**), u nového **New repository secret**, třikrát:

| Name | Hodnota |
|---|---|
| `YT_CLIENT_ID` | Client ID z kroku 2 |
| `YT_CLIENT_SECRET` | Client secret z kroku 2 |
| `YT_REFRESH_TOKEN` | Refresh token z kroku 3 |

Tyto hodnoty nikam jinam nepište (ani do chatu, ani do souborů v repu). Kdyby unikly, smažte OAuth klienta z kroku 2 a založte nový.

**Doporučené zabezpečení – environment jen pro `main`.** Workflow běží v environmentu `youtube`. Když tajemství přesunete do něj, dostane se k nim jen běh z `main`, tedy jen to, co jste zkontroloval a sloučil (žádná jiná větev ani upravený workflow v ní):

1. Settings → **Environments** → `youtube` (vznikne sám při prvním běhu; jinak New environment, název `youtube`).
2. **Deployment branches and tags** → Selected branches and tags → Add rule → `main`.
3. **Environment secrets** → Add secret: `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` (stejné hodnoty).
4. Settings → Secrets and variables → Actions → **smazat** tři repozitářová tajemství `YT_*`.

GitHub uložená tajemství zpátky neukáže – pokud hodnoty nemáte, Client ID a secret najdete v Google Cloud Console (krok 2) a nový refresh token vytvoříte v OAuth Playground (krok 3).

### 5. Zkouška

GitHub → **Actions → Nahrát na YouTube → Run workflow** → Díl nechat prázdný, zaškrtnout **Jen zkouška** (nebo **Jen přehled kanálu** – vypíše jazyky všech videí a playlistů) → Run. Zkouška nic nenahraje ani nezmění, ale přihlásí se k YouTube, vypíše název kanálu, ověří, že existují všechny playlisty z `kanal.json`, a vypíše jejich obsah čísly dílů, např. `hi: 09 09 01 02 03 04 05 07 · zdvojené: 09 · chybí: 06 08` (`?` = video, které repo nezná). Výsledek je v detailu běhu, v kroku „Nahrát na YouTube“.

## Běžné použití – nová jazyková verze

1. Claude nechá text namluvit workflow „Namluvit“ ([návod](../elevenlabs/NAVOD.md)), složí video a doplní jazyk do `youtube.json` dílu (soubor, název, popis, štítky) – vše ve větvi `claude/upravy`. Videa vám pošle ke kontrole.
2. Vy zkontrolujete a sloučíte pull request do `main`.
3. Sloučení spustí nahrání: videa se nahrají, naplánují a zařadí do playlistů (viz [Playlisty](#playlisty)). ID, termíny a záznam o playlistu se zapíšou do `youtube.json` v `main`.
4. V YouTube Studiu jen nastavíte související video (API to neumí).

Ručně: **Actions → Nahrát na YouTube → Run workflow** → Díl (např. `05`, víc dílů `01 02 03`, prázdné = všechny), Jazyky (např. `es hi`, prázdné = všechny), **Naplánovat zveřejnění** (zapnuté) nebo **Zveřejnit hned** → Run. Bez nich se video nahraje jako soukromé.

U starších dílů (01–08), jejichž české a anglické verze byly nahrané ručně, obsahuje `youtube.json` jen nové jazyky – jinak by je workflow nahrálo znovu.

Skript nikdy nenahraje jazyk, který už má v `youtube.json` vyplněné `videoId` (pokud se mu výslovně neřekne `--znovu`), takže omylem spuštěný workflow nic nezdvojí.

## Úprava už nahraných videí

Název, jazyk názvu a jazyk zvuku nahraných videí srovná podle `youtube.json` volba **Srovnat už nahraná videa s youtube.json** (Run workflow → Díl, Jazyky, zaškrtnout volbu). Popis a štítky doplní jen tam, kde na YouTube chybí; ručně napsaný popis nepřepisuje. Se zaškrtnutou **Jen zkouškou** jen vypíše, co by se změnilo (jde spustit i z jiné větve než `main`). Každé změněné video stojí 50 jednotek kvóty. Z příkazové řádky: `python3 aktualizuj.py 01 02 cs en --zkouska`.

## Playlisty

Každý běh projde playlisty dotčených jazyků (po sloučení a v denním běhu všech) a:

1. **smaže zdvojené položky** videí evidovaných v `youtube.json` (jedna zůstane),
2. **doplní evidovaná videa, která v playlistu chybí** – kromě těch, která už do něj jednou přidal (v `youtube.json` mají `"playlist": "<ID>"`); ručně odebrané video tak zpátky nevrací a zpožděný výpis playlistu nezpůsobí zdvojení,
3. **seřadí playlist podle čísla dílu** – jen když má playlist **ruční řazení** a obsahuje výhradně evidovaná videa (španělský, hindský, portugalský). Český a anglický obsahují ručně nahraná videa, ty nechává v pořadí, jaké mají; nová videa jen přidá na konec.

Playlist s **automatickým řazením** (podle data přidání nebo zveřejnění) přes API seřadit nejde – skript ho jen ohlásí: „playlist má automatické řazení“. Na ruční řazení ho přepnete na youtube.com: otevřít playlist a přetáhnout video na jiné místo (za úchyt vlevo od náhledu). Když YouTube nahoře hlásí „This is how your playlist looks in American English. Switch to Spanish to make changes“, je potřeba nejdřív přepnout jazyk YouTube (avatar → Language) na jazyk playlistu. Další běh pak pořadí srovná sám.

Skript nikdy nedělá dvojici „přidat znovu a smazat“ – každý krok je samostatně bezpečný, takže přerušený běh nenechá playlist rozbitý.

Jen údržba, bez nahrávání: **Run workflow** → Díl prázdný → Run (nahraje se jen to, co ještě nahrané není, tedy obvykle nic).

## Když běh zčervená

Červený běh znamená, že něco zůstalo nedokončené – v souhrnu běhu je řádek **Nedokončeno** (např. vyčerpaná kvóta, video nezařazené do playlistu). Co se nahrát stihlo, je zapsané v repu; zbytek dodělá další běh (nejpozději denní v 10:17 UTC). Opakuje-li se chyba i druhý den, je potřeba se podívat do výpisu.

## Limity

- YouTube Data API: nahrávání videí má vlastní limit (asi 100 denně na projekt). Ostatní volání sdílí denní kvótu 10 000 jednotek celého projektu (proto vlastní projekt jen pro nahrávání): výpis playlistu 1 jednotka, zařazení, přesun i smazání položky 50 – i když je požadavek odmítnutý. Kvóta se obnovuje o půlnoci kalifornského času (9:00 našeho času v zimě).
- Orientačně: běh s 29 novými videy v pěti jazycích ≈ 1 700 jednotek, denní běh bez novinek ≈ 20–70 jednotek. Spotřebu odhaduje skript na konci výpisu. Při vyčerpání kvóty počká minutu, zkusí to ještě jednou a pak další volání vynechá (dodělá je příští běh).
- Soubor `youtube.json`: název max. 100 znaků, popis max. 5 000 bajtů, bez znaků `<` a `>`.
