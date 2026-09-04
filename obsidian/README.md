# 🧪 Laboratoire IA multi-agents — vault Obsidian

Un mini-laboratoire visuel : **6 agents immobiles en cercle**, un orchestrateur au
centre, et des **bulles de communication** qui montrent ce qui transite entre eux.
Chaque agent est une fiche que tu peux ouvrir, lire et **modifier individuellement**.

## Ouvrir le vault
1. Obsidian → *Ouvrir un autre coffre* → **Ouvrir un dossier comme coffre**
2. Choisis ce dossier : `obsidian/`
3. Ouvre le fichier **`IA Multi-Agents.canvas`**

> ⚠️ Ouvre bien `obsidian/` comme racine du coffre, pas la racine du dépôt :
> les chemins du Canvas (`agents/agent-1-collecte.md`) sont relatifs à ce dossier.

## Contenu
```
obsidian/
├── IA Multi-Agents.canvas        ← la toile : cercle + centre + bulles
├── pipeline-orchestrateur.md     ← la carte du centre
├── agents/
│   ├── agent-1-collecte.md       🔵 liens Kick vérifiés
│   ├── agent-2-modification.md   🟢 stream modifié
│   ├── agent-3-decoupage.md      🟡 clips bruts
│   ├── agent-4-montage.md        🔴 short monté
│   ├── agent-5-verification.md   🟣 short validé + métadonnées
│   └── agent-6-publication.md    🩵 publication + performances
├── Tableau de bord.md            ← l'autonomie des 6 agents, régénéré
├── memoire/agent-1..6.json       ← la mémoire brute (écrite par le script)
├── journal/                      ← les cheminements, un par exécution
├── templates/
│   ├── agent.md                  ← le moule pour créer un nouvel agent
│   └── cheminement.md            ← le moule pour relire une exécution
├── avatars/                      ← les images statiques des personnages
└── outils/
    ├── generer-canvas.py         ← régénère la toile (cercle, positions, liens)
    └── apprendre.py              ← la boucle d'apprentissage des agents
```

## La disposition
```
                    🔵 Agent 1 — Collecte
       🩵 Agent 6                        🟢 Agent 2
       Publication      ⚙️ Pipeline /   Modification
                        Orchestrateur
       🟣 Agent 5                        🟡 Agent 3
       Vérification                       Découpage
                    🔴 Agent 4 — Montage
```
- **Cercle** : les 6 agents, à 60° d'écart, l'agent 1 à midi, sens horaire.
- **Centre** : l'orchestrateur, relié à chaque agent par un lien fin (supervision).
- **Bulles** : une carte flottante entre deux agents, à l'extérieur du cercle.
- **Boucle violette** : le feedback de l'Agent 5 vers les agents 1, 3 et 4.

## Le flux
| De → à | Bulle |
|---|---|
| Orchestrateur → Agent 1 | Chaînes Kick à suivre |
| Agent 1 → Agent 2 | Liens vérifiés + métadonnées |
| Agent 2 → Agent 3 | Stream modifié + passages |
| Agent 3 → Agent 4 | Clips bruts |
| Agent 4 → Agent 5 | Short monté |
| Agent 5 → Agent 6 | Short validé + métadonnées |
| Agent 6 → Orchestrateur | Publication + performances |
| Agent 5 → Agents 1 / 3 / 4 | Feedback de correction |

## Modifier le comportement d'un agent
Double-clic sur sa carte dans le Canvas → la fiche s'ouvre. Va dans la section
**🎛️ Zone de comportement (à modifier)** : le bloc ` ```prompt ` est son instruction
système, le tableau juste en dessous règle créativité, verbosité et strictesse.
Tout le reste de la fiche (rôle, compétences, livrables, mémoire) est de la
documentation : c'est ce bloc-là qui change ce que l'agent fait.

La section **🧬 Mémoire de l'agent** est faite pour être enrichie à la main après
chaque exécution : règle apprise, erreur constatée, correction appliquée.

## Le cheminement — comment on trouve l'erreur

Un agent qui rend seulement son résultat est un agent qu'on ne peut pas corriger :
on voit le symptôme, jamais la cause. Alors chaque agent doit d'abord écrire
**comment il y est arrivé**, en six sections :

| Section | Ce qu'elle révèle |
|---|---|
| 1. Reçu | a-t-il eu la bonne matière au départ ? |
| 2. Compris | a-t-il compris autre chose que ce qu'on demandait ? |
| 3. Étapes | en a-t-il sauté une, ou inversé deux ? |
| **4. Décisions** | **a-t-il choisi pour une mauvaise raison ?** |
| **5. Doutes** | **a-t-il tranché au hasard là où il fallait demander ?** |
| 6. Rendu | a-t-il rendu autre chose que ce qui était attendu ? |

L'erreur est presque toujours en 4 ou en 5.

Ce protocole n'est écrit **qu'une seule fois**, dans la constante `PROTOCOLE` de
`outils/apprendre.py`, et il est ajouté au prompt des six agents à chaque
régénération. Tu le modifies là, ils l'ont tous.

Les cheminements se rangent dans `journal/`, sur le modèle de
`templates/cheminement.md`. Voir `journal/README.md`.

## La boucle d'apprentissage

Un agent ne s'améliore pas tout seul : il s'améliore parce qu'on lui écrit ce qu'il
a raté. C'est exactement ce que fait `outils/apprendre.py`, et c'est le cœur du
laboratoire.

### Les deux seules choses à faire

```bash
# l'agent a bien travaillé
python3 outils/apprendre.py succes --agent 3

# l'agent s'est trompé
python3 outils/apprendre.py lecon --agent 3 \
    --erreur "clip coupé au milieu du mot « exactement » à 00:04:12" \
    --regle "vérifier la frontière de mot sur les 5 dernières frames" \
    --gravite bloquant --source agent-5
```

### Ce qui se passe alors

1. La leçon est écrite dans `memoire/agent-3.json`.
2. La fiche `agents/agent-3-decoupage.md` est réécrite : la règle apparaît dans
   **Règles apprises**, l'erreur dans **Erreurs passées**.
3. Si la gravité est `bloquant`, **la règle est ajoutée au prompt de l'agent** —
   il la portera dans toutes ses exécutions suivantes. C'est ça, corriger.
4. La série d'exécutions propres repart de zéro. Le `Tableau de bord.md` est
   régénéré.

### Mesurer l'autonomie

Un agent est **autonome** quand il enchaîne son objectif d'exécutions sans le
moindre incident — 10 par défaut. C'est une définition volontairement dure :
la série retombe à zéro au premier faux pas.

| Jauge | Statut | Ce que ça veut dire |
|---|---|---|
| 🟥 | en rodage | il faut le surveiller à chaque passage |
| 🟧 | en progrès | il tient, mais pas encore longtemps |
| 🟨 | presque | on peut commencer à le laisser seul |
| 🟩 | autonome | objectif atteint, il tourne seul |

```bash
python3 outils/apprendre.py etat      # l'état des 6 agents en une vue
python3 outils/apprendre.py fiches    # tout régénérer après une modif à la main
```

### Les zones écrites par le script

Dans chaque fiche, trois zones sont encadrées par des marqueurs :

```
<!-- MEMOIRE:DEBUT -->  …  <!-- MEMOIRE:FIN -->
<!-- PROMPT:DEBUT -->   …  <!-- PROMPT:FIN -->
<!-- AUTONOMIE:DEBUT -->…  <!-- AUTONOMIE:FIN -->
```

Le script ne touche **qu'à l'intérieur** de ces zones. Tout le reste de la fiche
— rôle, compétences, livrables, fonctions, contraintes dures — reste à toi, tu
peux l'écrire à la main dans Obsidian sans rien risquer.

Le prompt de base d'un agent (celui d'avant tout apprentissage) vit dans
`memoire/agent-N.json`, clé `prompt_base` : c'est là qu'on le change, pas dans la
fiche, sinon la prochaine régénération l'écrase.

## Ajouter un 7ᵉ agent
1. Copie `templates/agent.md` dans `agents/agent-7-xxx.md` et remplis les `{{...}}`.
2. Crée sa mémoire `memoire/agent-7.json` sur le modèle des autres
   (`agent`, `nom`, `prompt_base`, `lecons: []`, `ameliorations: []`, `notes`,
   `autonomie`), puis lance `python3 outils/apprendre.py fiches`.
3. Ajoute-le dans la liste `AGENTS` de `outils/generer-canvas.py` (id, fichier,
   couleur hex, libellé de la bulle sortante) et dans le dictionnaire `SUIVANT`.
4. Relance depuis la racine du coffre :
   ```bash
   python3 outils/generer-canvas.py
   ```
   Le cercle est recalculé automatiquement pour le nouveau nombre d'agents.

> Régénérer écrase `IA Multi-Agents.canvas` : si tu as déplacé des cartes à la main
> dans Obsidian, tes positions seront perdues. Modifie plutôt le script (ou fais une
> copie de la toile avant).

## Avatars
Voir `avatars/README.md` : nommage, prompts de génération et deux façons de
rattacher une image statique à la carte d'un agent.
