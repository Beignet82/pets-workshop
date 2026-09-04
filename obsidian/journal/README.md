# 📓 Journal des cheminements

Un fichier par exécution d'agent. C'est ici qu'on retrouve les erreurs.

## Pourquoi
Chaque agent doit écrire **comment il est arrivé à son résultat** avant de rendre
le résultat lui-même : ce qu'il a reçu, ce qu'il a compris, ses étapes, ses
décisions, ses doutes. Un agent qui rend juste un livrable est un agent dont on
ne peut pas corriger le raisonnement — on ne voit que le symptôme.

## Comment s'en servir
1. L'agent tourne et écrit son cheminement.
2. Tu le colles dans un nouveau fichier ici, sur le modèle de
   `templates/cheminement.md`.
3. Tu lis les six sections. **L'erreur est presque toujours à l'étape 4 ou 5** :
   une décision prise pour une mauvaise raison, ou un doute résolu au hasard.
4. Tu remplis la section « Ma relecture » en bas.
5. Tu me le dis, et j'écris la leçon dans la mémoire de l'agent :
   ```bash
   python3 outils/apprendre.py lecon --agent N --erreur "…" --regle "…" --gravite bloquant
   ```

## Nommage
```
journal/2026-09-04-agent-1-lien-01.md
journal/2026-09-04-agent-2-passe-01.md
```

## Où lire l'erreur
| Section | Ce qu'elle révèle |
|---|---|
| 1. Reçu | l'agent a-t-il eu la bonne matière au départ ? |
| 2. Compris | a-t-il compris autre chose que ce qu'on demandait ? |
| 3. Étapes | en a-t-il sauté une, ou inversé deux ? |
| **4. Décisions** | **a-t-il choisi pour une mauvaise raison ?** |
| **5. Doutes** | **a-t-il tranché au hasard là où il fallait demander ?** |
| 6. Rendu | a-t-il rendu autre chose que ce qui était attendu ? |
