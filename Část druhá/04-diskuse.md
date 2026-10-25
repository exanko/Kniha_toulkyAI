# Diskuse recenzentů s autorem – Část druhá

*Follow-up rozhovory: autor odpovídá na výtky recenzentů a recenzenti reagují.*

## Inkling

**Téma:** Je workflow jen marketingový leták?
*Navazuje na výtku Inklingu, že praktický workflow v kapitole 4 je „příliš obecný a působí jako vložený marketingový leták“.*

**Autor:** Jak tedy workflow z letáku převést na praxi? Nebo je to pouhá autorova reklama na technicky nefunkční stroj?

**Inkling:** Není to reklama – workflow je funkční, ale zjednodušený pro 1–2 lidi. Prakticky: jeden Git repo = single source of truth, agent (např. Claude/Codex v CLI) má přístup, v repo SKILL.md + markdown dokumenty, PDF generuje agent při commitu, záloha do Git. Funguje to; limit je škálování – pro větší firmu chybí RBAC, databáze, audit, jak autor sám říká v kap. 8. Takže stroj funguje, ale není univerzální.

**Autor:** A není toto právě závěrem knihy?

**Inkling:** Ano – přesně to je bod 8. Workflow funguje pro 1–2 lidi, ale závěr knihy říká: když projekt vyroste, starý postup přestane stačit a musíš postavit robustní systém s databází, rolemi a vlastními asistenty. Autor to sám uzavírá.

---

[← Závěr: Velcí a malí recenzenti](03-velci-a-mali-recenzenti.md) · [Obsah](01-obsah.md)
