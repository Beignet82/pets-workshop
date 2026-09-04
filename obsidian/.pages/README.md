# Pages web du laboratoire

Les sources des deux pages publiées. Le dossier commence par un point : Obsidian
l'ignore, il n'apparaît donc pas dans le coffre.

| Fichier | Page | À quoi elle sert |
|---|---|---|
| `cercle-agents.html` | Le cercle des agents | voir les 6 agents en orbite, lire leur fiche, copier une fiche vers Obsidian |
| `construire-le-labo.html` | Construire le labo | les 14 étapes pour bâtir le coffre à la main |

`cercle-agents.html` porte sa propre copie des fiches d'agents. Elle est
**générée depuis `memoire/agent-N.json`**, jamais écrite à la main : après avoir
changé un prompt, il faut la resynchroniser, sinon la page affiche et fait
copier un agent qui n'existe plus. C'est déjà arrivé une fois.
