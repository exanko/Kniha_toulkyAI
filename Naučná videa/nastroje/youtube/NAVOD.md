# Nahrávání na YouTube přes GitHub Actions

Workflow **„Nahrát na YouTube“** nahraje jazykové verze dílu podle souboru `Naučná videa/<díl>/youtube.json` (název, popis, štítky, soubor), zařadí je do playlistu jazyka (`kanal.json`) a ID videa zapíše zpátky do repa. Videa se nahrávají jako **soukromá**; zveřejníte je v YouTube Studiu.

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

### 5. Zkouška

GitHub → **Actions → Nahrát na YouTube → Run workflow** → Díl `09`, zaškrtnout **Jen zkouška** → Run. Zkouška nic nenahraje, ale přihlásí se k YouTube, vypíše název kanálu a ověří, že existují všechny playlisty z `kanal.json`. Má projít zeleně (jazyky dílu 09 už jsou nahrané, takže se jen přeskočí). Výsledek je v detailu běhu, v kroku „Nahrát na YouTube“.

## Běžné použití – nová jazyková verze

1. Claude připraví text, vy ho namluvíte v ElevenLabs a pošlete MP3.
2. Claude složí video a doplní jazyk do `youtube.json` dílu (soubor, název, popis, štítky).
3. Vy: **Actions → Nahrát na YouTube → Run workflow** → Díl (např. `05`), Jazyky (např. `es hi`, prázdné = všechny dosud nenahrané) → Run. Jde to i z mobilní aplikace GitHubu.
4. V YouTube Studiu video zkontrolujete, nastavíte související video a zveřejníte.

U starších dílů (01–08), jejichž české a anglické verze byly nahrané ručně, obsahuje `youtube.json` jen nové jazyky – jinak by je workflow nahrálo znovu.

Skript nikdy nenahraje jazyk, který už má v `youtube.json` vyplněné `videoId` (pokud se mu výslovně neřekne `--znovu`), takže omylem spuštěný workflow nic nezdvojí.

## Limity

- YouTube Data API: až 100 nahrání denně na projekt; zařazení do playlistu bere 50 jednotek z denní kvóty 10 000 (sdílené se streamováním).
- Soubor `youtube.json`: název max. 100 znaků, popis max. 5 000 bajtů, bez znaků `<` a `>`.
