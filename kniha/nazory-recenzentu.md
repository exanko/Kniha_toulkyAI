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

---

[← Recenze](recenze.md) · [Obsah](01-obsah.md)
