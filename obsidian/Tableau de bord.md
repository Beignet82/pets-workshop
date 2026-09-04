---
tags: [tableau-de-bord, pipeline-shorts]
---

# 📊 Tableau de bord — autonomie des agents

*Mis à jour le 2026-09-04.* Ce fichier est régénéré automatiquement :
ne l'écris pas à la main, il serait écrasé.

| Agent | Statut | Progression | Série | Incidents | Dernière leçon |
|---|---|---|---|---|---|
| [[agent-1-ingestion|1 — Ingestion & Transcription]] | 🟥 en rodage | ▱▱▱▱▱▱▱▱▱▱ | 0 / 10 | 2 | 2026-09-04 |
| [[agent-2-analyse|2 — Analyse & Détection des moments forts]] | 🟥 en rodage | ▱▱▱▱▱▱▱▱▱▱ | 0 / 10 | 2 | 2026-09-04 |
| [[agent-3-decoupage|3 — Découpage & Extraction des clips]] | 🟥 en rodage | ▱▱▱▱▱▱▱▱▱▱ | 0 / 10 | 2 | 2026-09-04 |
| [[agent-4-montage|4 — Montage & Habillage]] | 🟥 en rodage | ▱▱▱▱▱▱▱▱▱▱ | 0 / 10 | 2 | 2026-09-04 |
| [[agent-5-verification|5 — Vérification & Contrôle qualité]] | 🟥 en rodage | ▱▱▱▱▱▱▱▱▱▱ | 0 / 10 | 2 | 2026-09-04 |
| [[agent-6-publication|6 — Publication & Diffusion]] | 🟥 en rodage | ▱▱▱▱▱▱▱▱▱▱ | 0 / 10 | 2 | 2026-09-04 |

**0 agent(s) sur 6 au niveau autonome.**

## Comment ça bouge

| Ce qui arrive | La commande | L'effet |
|---|---|---|
| L'agent a bien travaillé | `succes --agent N` | la série avance |
| L'agent s'est trompé | `lecon --agent N --erreur … --regle …` | la série repart de zéro, la règle est écrite |
| La règle est grave | `--gravite bloquant` | la règle entre dans le prompt de l'agent |

Les fiches sont dans `agents/`, la mémoire brute dans `memoire/`.
