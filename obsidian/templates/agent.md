---
agent_id: {{agent_id}}
ordre: {{ordre}}
couleur: {{couleur}}
statut: actif
tags: [agent, pipeline-shorts]
---

# {{title}}

## 🧠 Rôle
{{role}}

## 🎯 Compétences
- {{competence1}}
- {{competence2}}
- {{competence3}}

## 📦 Livrables
- {{livrable1}}
- {{livrable2}}
- {{livrable3}}

## 📊 Autonomie
<!-- AUTONOMIE:DEBUT -->
<!-- AUTONOMIE:FIN -->

## 🧬 Mémoire de l'agent
<!-- MEMOIRE:DEBUT -->
<!-- MEMOIRE:FIN -->

## ⚙️ Fonctions

### Entraîner
```
{{training_logic}}
```

### Tester
```
{{testing_logic}}
```

### Exécuter
```
{{run_logic}}
```

### Améliorer
```
{{improve_logic}}
```

## 🎛️ Zone de comportement (à modifier)
> C'est ici que tu modifies l'agent. Tout ce qui est dans ce bloc est lu comme instruction système.

<!-- PROMPT:DEBUT -->
```prompt
{{system_prompt}}
```
<!-- PROMPT:FIN -->

| Paramètre | Valeur | Effet |
|---|---|---|
| Créativité | {{creativite}} | 0 = strict, 1 = libre |
| Verbosité | {{verbosite}} | courte / normale / détaillée |
| Strictesse | {{strictesse}} | tolérance aux erreurs |
| Modèle | {{modele}} | moteur utilisé |

### Contraintes dures (ne jamais violer)
- {{contrainte1}}
- {{contrainte2}}

### Critères de réussite
- {{critere1}}
- {{critere2}}

## 🔗 Communication
Reçoit de : {{input_from}}
Envoie à : {{output_to}}

## 🖼️ Image descriptive
*(Décris ici l'image que tu veux associer à cet agent)*

---

> Les zones `<!-- … :DEBUT -->` … `<!-- … :FIN -->` sont écrites par
> `outils/apprendre.py`. N'écris pas dedans à la main : le script les écrase.
> Tout le reste de la fiche t'appartient.
