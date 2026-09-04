# 🖼️ Avatars des agents

Chaque agent est un **personnage immobile** : une image statique, pas d'animation.
Dépose ici les fichiers, puis rattache-les aux cartes du Canvas.

## Nommage attendu
```
avatars/agent-1-ingestion.png
avatars/agent-2-analyse.png
avatars/agent-3-decoupage.png
avatars/agent-4-montage.png
avatars/agent-5-verification.png
avatars/agent-6-publication.png
avatars/orchestrateur.png
```

## Rattacher un avatar à une carte
Deux options :

1. **Dans la fiche de l'agent** — ajoute la ligne sous le titre :
   `![[agent-1-ingestion.png|120]]`
   L'image apparaît directement dans la carte du Canvas.

2. **Dans le Canvas** — glisse l'image depuis l'explorateur sur la toile,
   place-la à côté de la carte de l'agent, puis relie-la (lien court, sans libellé).

## Prompts de génération (styles cohérents entre les 6)
Base commune : *personnage stylisé de face, immobile, buste, fond transparent,
aplats de couleur, contour net, style vectoriel plat, pas de texte.*

| Agent | Prompt |
|---|---|
| 1 — Ingestion | personnage **bleu**, casque audio sur les oreilles, ondes sonores fines autour de la tête |
| 2 — Analyse | personnage **vert**, loupe à la main, petites barres de score lumineuses flottantes |
| 3 — Découpage | personnage **jaune**, ciseau de montage, bande de pellicule découpée en segments |
| 4 — Montage | personnage **rouge**, timeline de montage flottante, calques vidéo empilés |
| 5 — Vérification | personnage **violet**, checklist lumineuse, tampon « validé » en main |
| 6 — Publication | personnage **turquoise**, petit satellite au-dessus de la tête, icônes de plateformes en orbite |
| Orchestrateur | figure **grise** centrale, six fils lumineux tendus vers l'extérieur |
