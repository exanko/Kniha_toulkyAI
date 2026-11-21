# Nahrávání na YouTube přes GitHub Actions

Workflow **„Nahrát na YouTube“** nahraje jazykové verze dílu podle souboru `Naučná videa/<díl>/youtube.json` (název, popis, štítky, soubor), zařadí je do playlistu jazyka (`kanal.json`) a ID videa zapíše zpátky do repa.

**Spouští se samo po sloučení do `main`**, když se změní některý `youtube.json`: nahraje všechno, co ještě nemá `videoId`, a **naplánuje zveřejnění** – v každém jazyce jedno video denně (od zítřka, nebo den po posledním naplánovaném), v čase z `kanal.json`: CZ 18:00 Praha, EN 12:00 New York, ES 18:00 Ciudad de México, HI 18:00 Indie. Konkrétní termín jde předepsat v `youtube.json` (`"zverejneni": "2026-12-01T18:00"`). Do té doby jsou videa soukromá a v YouTube Studiu je vidíte jako naplánovaná.

Co zůstává ruční (YouTube to přes API nedovolí): **související video** u Shortu a **vlastní miniatura** u Shortu.

## Jednorázové nastavení (asi 15 minut)

Použijte stávající projekt v Google Cloud, ve kterém už máte zapnuté **YouTube Data API v3**.

### 1. Stav publikování na „In production“

Google Cloud Console → **Google Auth Platform → Audience** (dříve „OAuth consent screen“).

- Pokud je **Publishing status: Testing**, klikněte na **Publish app**. V režimu Testing přihlášení po 7 dnech vyprší a nahrávání by přestalo fungovat.
- Ověřování aplikace u Googlu není potřeba – pro vlastní účet stačí, že se při přihlášení jednou odklikne varování „Google tuto aplikaci neověřil“.

### 2. Nový OAuth klient jen pro nahrávání

**Google Auth Platform → Clients → Create client** (dříve Credentials → Create credentials → OAuth client ID):

- **Application type:** Web application
- **Name:** např. `GitHub Actions – nahrávání`
- **Authorized redirect URIs:** `https://developers.google.com/oauthplayground`

Po vytvoření si zkopírujte **Client ID** a **Client secret**. (Klienta pro streamování nechte, jak je – každý nástroj má svého.)

### 3. Obnovovací token (refresh token) přes OAuth Playground

1. Otevřete https://developers.google.com/oauthplayground
2. Vpravo nahoře ozubené kolo (OAuth 2.0 configuration): zaškrtněte **Use your own OAuth credentials**, vložte Client ID a Client secret z kroku 2, **Access type: Offline**. Zavřete.
3. Vlevo do pole „Input your own scopes“ vložte `https://www.googleapis.com/auth/youtube` a klikněte **Authorize APIs**.
4. Přihlaste se účtem, kterému patří kanál (u kanálu pod značkovým účtem vyberte kanál). U varování „Google tuto aplikaci neověřil“ → **Rozšířené → Přejít na…** → **Povolit**.
5. **Step 2 → Exchange authorization code for tokens** → zkopírujte **Refresh token**.

### 4. Tajemství v GitHubu

Repozitář na GitHubu → **Settings → Secrets and variables → Actions → New repository secret**, třikrát:

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

GitHub → **Actions → Nahrát na YouTube → Run workflow** → Díl `09`, zaškrtnout **Jen zkouška** → Run. Zkouška nic nenahraje, ale přihlásí se k YouTube, vypíše název kanálu a ověří, že existují všechny playlisty z `kanal.json`. Má projít zeleně (jazyky dílu 09 už jsou nahrané, takže se jen přeskočí). Vypíše také, jestli playlisty mají správné pořadí. Výsledek je v detailu běhu, v kroku „Nahrát na YouTube“.

## Běžné použití – nová jazyková verze

1. Claude nechá text namluvit workflow „Namluvit“ ([návod](../elevenlabs/NAVOD.md)), složí video a doplní jazyk do `youtube.json` dílu (soubor, název, popis, štítky) – vše ve větvi `claude/upravy`. Videa vám pošle ke kontrole.
2. Vy zkontrolujete a sloučíte pull request do `main`.
3. Sloučení spustí nahrání: videa se nahrají, naplánují, zařadí do playlistů a playlisty se seřadí podle čísel dílů (viz [Pořadí v playlistu](#pořadí-v-playlistu)). ID a termíny se zapíšou do `youtube.json` v `main`.
4. V YouTube Studiu jen nastavíte související video (API to neumí).

Ručně: **Actions → Nahrát na YouTube → Run workflow** → Díl (např. `05`, nebo víc dílů: `01 02 03`), Jazyky (např. `es hi`, prázdné = všechny dosud nenahrané), případně **Naplánovat zveřejnění** nebo **Zveřejnit hned** → Run. Bez nich se video nahraje jako soukromé.

U starších dílů (01–08), jejichž české a anglické verze byly nahrané ručně, obsahuje `youtube.json` jen nové jazyky – jinak by je workflow nahrálo znovu.

Skript nikdy nenahraje jazyk, který už má v `youtube.json` vyplněné `videoId` (pokud se mu výslovně neřekne `--znovu`), takže omylem spuštěný workflow nic nezdvojí.

## Pořadí v playlistu

Na konci každého běhu skript seřadí playlisty zvolených jazyků podle čísla dílu (01, 02, … 09). Řadí jen playlist, ve kterém jsou výhradně videa evidovaná v `youtube.json` – tedy španělský a hindský. Český a anglický obsahují ručně nahraná videa, takže je nechá být.

- Playlist s ručním řazením: videa jen přesune.
- Playlist bez něj (jako ten španělský): video, které není na svém místě, přidá znovu na konec ve správném pořadí a starou položku smaže až potom, takže z playlistu nikdy nezmizí. Musí přitom zůstat vypnuté nastavení playlistu **Add new videos to top of playlist** („Přidávat nová videa na začátek“).

Jen srovnat, bez nahrávání: **Run workflow** → Díl `09`, Jazyky `es` (nebo `hi`) → Run. Díl 09 už je nahraný, takže se jen přeskočí a srovná se playlist.

Ručně: na stránce playlistu na YouTube video chytit a přetáhnout. Když YouTube nahoře hlásí „This is how your playlist looks in American English. Switch to Spanish to make changes“, je potřeba nejdřív přepnout jazyk YouTube (avatar → Language) na jazyk playlistu.

## Limity

- YouTube Data API: až 100 nahrání denně na projekt; zařazení, přesun i smazání položky playlistu bere 50 jednotek z denní kvóty 10 000 (sdílené se streamováním); srovnání celého španělského playlistu tak stojí nejvýš asi 700 jednotek.
- Soubor `youtube.json`: název max. 100 znaků, popis max. 5 000 bajtů, bez znaků `<` a `>`.
