#!/usr/bin/env python3
"""Assemble tout le laboratoire en UNE seule note Markdown.

Sert quand on ne peut pas installer un coffre complet : un seul fichier à
glisser dans Obsidian, ou à copier-coller dans une note vide. On y perd la
toile Canvas et les liens entre fiches, on y gagne de pouvoir commencer
tout de suite, sur n'importe quel appareil.

    python3 outils/exporter-note-unique.py
"""

import glob
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "Labo-agents-tout-en-un.md")


def nettoyer(chemin):
    """Le contenu du fichier, sans son frontmatter ni les marqueurs de zone."""
    texte = open(chemin, encoding="utf-8").read()
    texte = re.sub(r"\A---\n.*?\n---\n+", "", texte, flags=re.DOTALL)
    texte = re.sub(r"^<!-- \w+:(DEBUT|FIN) -->\n", "", texte, flags=re.MULTILINE)
    return texte.strip()


def titre_de(texte):
    m = re.search(r"^# (.+)$", texte, re.MULTILINE)
    return m.group(1) if m else "Sans titre"


fiches = sorted(glob.glob(os.path.join(RACINE, "agents", "agent-*.md")))
morceaux = [nettoyer(f) for f in fiches]
orchestrateur = nettoyer(os.path.join(RACINE, "pipeline-orchestrateur.md"))
tableau = nettoyer(os.path.join(RACINE, "Tableau de bord.md"))

entete = """---
tags: [laboratoire, pipeline-shorts, kick]
---

# 🧪 Laboratoire IA multi-agents — tout en un

> Cette note contient **la totalité du laboratoire** : les six agents,
> l'orchestrateur et le tableau de bord. Rien d'autre à installer.
> Tu peux la couper en plusieurs notes plus tard, quand tu seras à l'aise.

## Ce que tu peux modifier

Dans chaque agent, cherche la section **🎛️ Zone de comportement**. Le bloc
` ```prompt ` qu'elle contient est **la seule chose qui change ce que fait
l'agent**. Tout le reste est de la documentation : utile à lire, sans effet.

Chaque prompt se termine par le même **protocole de cheminement** : l'agent
doit écrire comment il est arrivé à son résultat avant de le rendre. C'est ce
qui rend l'erreur trouvable — elle est presque toujours dans ses décisions ou
dans ses doutes, pas dans ses étapes.

## Le pipeline

| # | Agent | Ce qu'il transmet au suivant |
|---|---|---|
| 1 | Collecte des liens Kick | liens vérifiés + métadonnées |
| 2 | Modification des streams | stream modifié + passages retenus |
| 3 | Découpage | clips bruts |
| 4 | Montage | short monté |
| 5 | Vérification | short validé + métadonnées |
| 6 | Publication | publication + performances |

L'agent 5 peut renvoyer un travail aux agents 1, 3 et 4 : c'est la boucle de
correction. L'agent 6 rend compte à l'orchestrateur.

## Sommaire
"""

sommaire = "\n".join(f"- [[#{titre_de(m)}]]" for m in morceaux)
sommaire += f"\n- [[#{titre_de(orchestrateur)}]]\n- [[#{titre_de(tableau)}]]\n"

corps = "\n\n---\n\n".join(morceaux + [orchestrateur, tableau])

with open(SORTIE, "w", encoding="utf-8") as f:
    f.write(entete + sommaire + "\n---\n\n" + corps + "\n")

taille = os.path.getsize(SORTIE) / 1024
print(f"{SORTIE} · {len(morceaux) + 2} sections · {taille:.0f} Ko")
