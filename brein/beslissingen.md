# Beslissingen — logboek

> Belangrijke keuzes en het waarom. Nieuwste bovenaan. Houd het kort: beslissing → reden.

## 2026-06-17
- **Obsidian als mens-brein, niet als machine-geheugen.** Obsidian heeft geen officiële hosted MCP en vereist een draaiende app/pc → te fragiel als ruggengraat. We gebruiken het bovenop onze Git-versiebeheerde Markdown (`brein/`). Machine-geheugen blijft in JSON/Data Tables/Postgres.
- **n8n is de automation-ruggengraat.** Al gekoppeld; Anthropic + OpenAI credentials aanwezig. Eerste research-workflow (v1) gebouwd: gids → Claude extract+kwalificeer → prospects.
- **Kaart-view = Fase 1 af.** Dekkingskaart in dashboard (NL-provinciekaart, heatmap naar voortgang, filter per niche).

## 2026-06-16
- **Wildcard-cert voor `*.demo.brabantdigital.nl`** i.p.v. losse certs (Let's Encrypt-limiet van 50/week werd geraakt). Handmatig verlengen vóór 14-09-2026.
- **autodeploy robuust gemaakt** (geen abort bij 1 klant-fout; ruimt clones op). `scan-replies.py` corrumpeert `niet-deployen.txt` niet meer.
- **Kapper-niche + 2 premium-designs** (donker à la Mari, licht à la Asya). new-client.py herkent niche → juiste generator + label.
- **Autopilot-instelling server-persistent** (overal gelijk). Replies zichtbaar in dashboard-Activiteit.
- **Contactregel:** prospect = 06-mobiel óf e-mail óf social; vaste-lijn-only telt niet. Nooit gegevens verzinnen (autopilot mailt echte mensen).

## 2026-06-15
- **Outreach via mailrelay (mail.zxcs.nl)** — SPF/DKIM kloppen; VPS niet aan SPF toevoegen.
- **Prospect-velden regel:** compliment/gratis_tip/verbeteringen netjes per niche; nooit notitie/website-status in de tip.
