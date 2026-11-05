# Kniha Toulky AI – pravidla pro Clauda

- **Větve:** Claude pracuje jen ve větvi `claude/upravy`. Do `main` nic neposílá, pokud mu to autor výslovně neřekne; autor slučuje přes pull request.
- **Úpravy textu knihy:** jen gramatika, pravopis, interpunkce a rozčlenění do odstavců/seznamů. **Neměnit formulace vět, čísla, termíny ani fakta** a nepřidávat vlastní zvýraznění. Nejasná místa vypsat autorovi, ne opravovat.
- **Recenze a diskuse:** texty recenzentů vkládat doslova (jen typografie: české uvozovky „…“, pomlčky –), včetně jejich chyb; případné chyby jen zmínit autorovi.
- **Struktura:** `Část první/`, `Část druhá/` (00 úvodní strana, 01 obsah, 02 recenze, …, `kapitoly/`, `obrazky/`), `Naučná videa/`. Po každé změně zkontrolovat odkazy a obrázky.
- **Commity:** končit řádky `Co-Authored-By` a `Claude-Session` podle aktuálního pokynu prostředí.
- **Naučná videa:** postup je ve skillu `.claude/skills/naucne-video/SKILL.md`, pravidla série v `Naučná videa/README.md`.
