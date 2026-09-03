#!/usr/bin/env python3
"""Génère le Canvas Obsidian « IA Multi-Agents » : 6 agents en cercle,
orchestrateur au centre, bulles de communication sur les liens.

Usage :  python3 outils/generer-canvas.py   (depuis la racine du vault)
Modifie RAYON_AGENTS / RAYON_BULLES pour resserrer ou élargir le cercle.
"""

import json
import math
import os

RAYON_AGENTS = 1050
RAYON_BULLES = 1650
L_AGENT, H_AGENT = 420, 340
L_BULLE, H_BULLE = 300, 120
SORTIE = "IA Multi-Agents.canvas"

AGENTS = [
    # (id, fichier, couleur, libellé de la bulle sortante)
    ("a1", "agents/agent-1-ingestion.md",   "#2b6cff", "Transcript + timecodes"),
    ("a2", "agents/agent-2-analyse.md",     "#22a06b", "Moments forts + scoring"),
    ("a3", "agents/agent-3-decoupage.md",   "#e5b800", "Clips bruts"),
    ("a4", "agents/agent-4-montage.md",     "#e03131", "Short monté"),
    ("a5", "agents/agent-5-verification.md", "#8b5cf6", "Short validé + métadonnées"),
    ("a6", "agents/agent-6-publication.md", "#0fb5b5", "Publication + performances"),
]

# Le dernier maillon ne boucle pas sur l'agent 1 : il rend compte au centre.
SUIVANT = {"a1": "a2", "a2": "a3", "a3": "a4",
           "a4": "a5", "a5": "a6", "a6": "orchestrateur"}
COURT = {"orchestrateur": "ORCH."}


def place(angle_deg, rayon, largeur, hauteur):
    """Coin haut-gauche d'une carte centrée sur le cercle à cet angle."""
    a = math.radians(angle_deg)
    cx, cy = rayon * math.cos(a), rayon * math.sin(a)
    return int(round(cx - largeur / 2)), int(round(cy - hauteur / 2))


def centre(node):
    return node["x"] + node["width"] / 2, node["y"] + node["height"] / 2


def cotes(depuis, vers):
    """Choisit les faces d'accroche du lien selon la direction dominante."""
    dx = centre(vers)[0] - centre(depuis)[0]
    dy = centre(vers)[1] - centre(depuis)[1]
    if abs(dx) >= abs(dy):
        return ("right", "left") if dx > 0 else ("left", "right")
    return ("bottom", "top") if dy > 0 else ("top", "bottom")


nodes, edges = [], {}
index = {}

# --- Orchestrateur au centre -------------------------------------------------
orch = {
    "id": "orchestrateur",
    "type": "file",
    "file": "pipeline-orchestrateur.md",
    "x": -240, "y": -140, "width": 480, "height": 280,
    "color": "#6b7280",
}
nodes.append(orch)
index["orchestrateur"] = orch

# --- Les 6 agents, répartis à 60° d'écart, agent 1 en haut -------------------
for i, (aid, fichier, couleur, _) in enumerate(AGENTS):
    angle = -90 + i * 60          # -90° = midi, sens horaire
    x, y = place(angle, RAYON_AGENTS, L_AGENT, H_AGENT)
    n = {
        "id": aid, "type": "file", "file": fichier,
        "x": x, "y": y, "width": L_AGENT, "height": H_AGENT,
        "color": couleur,
    }
    nodes.append(n)
    index[aid] = n

# --- Bulles de communication, posées entre deux agents, à l'extérieur --------
for i, (aid, _, couleur, bulle) in enumerate(AGENTS):
    suivant = SUIVANT[aid]
    angle = -90 + i * 60 + 30     # à mi-chemin entre les deux agents
    x, y = place(angle, RAYON_BULLES, L_BULLE, H_BULLE)
    bid = f"bulle-{aid}-{suivant}"
    n = {
        "id": bid, "type": "text",
        "text": f"💬 **{bulle}**\n`{aid.upper()} → {COURT.get(suivant, suivant.upper())}`",
        "x": x, "y": y, "width": L_BULLE, "height": H_BULLE,
        "color": couleur,
    }
    nodes.append(n)
    index[bid] = n

# --- Légende ----------------------------------------------------------------
nodes.append({
    "id": "legende", "type": "text",
    "x": -2400, "y": -1500, "width": 460, "height": 460,
    "text": (
        "## 🧪 Laboratoire IA multi-agents\n\n"
        "**Cercle** : 6 agents immobiles, un rôle chacun.\n"
        "**Centre** : le pipeline / orchestrateur.\n"
        "**Bulles** : ce qui transite d'un agent au suivant.\n\n"
        "| | Agent |\n|---|---|\n"
        "| 🔵 | 1 — Ingestion |\n"
        "| 🟢 | 2 — Analyse |\n"
        "| 🟡 | 3 — Découpage |\n"
        "| 🔴 | 4 — Montage |\n"
        "| 🟣 | 5 — Vérification |\n"
        "| 🩵 | 6 — Publication |\n\n"
        "Double-clic sur une carte pour ouvrir la fiche de l'agent "
        "et modifier son comportement.\n\n"
        "Nouvel agent → copier `templates/agent.md`."
    ),
})

# --- Liens : chaîne principale, spokes de supervision, boucle de feedback ----
def lien(eid, depuis, vers, label=None, couleur=None):
    de, ve = cotes(index[depuis], index[vers])
    e = {"id": eid, "fromNode": depuis, "fromSide": de,
         "toNode": vers, "toSide": ve}
    if label:
        e["label"] = label
    if couleur:
        e["color"] = couleur
    edges[eid] = e

liens = []
# chaîne : agent i -> sa bulle -> agent i+1
for i, (aid, _, couleur, bulle) in enumerate(AGENTS):
    suivant = SUIVANT[aid]
    bid = f"bulle-{aid}-{suivant}"
    lien(f"e-{aid}-{bid}", aid, bid, None, couleur)
    lien(f"e-{bid}-{suivant}", bid, suivant, None, couleur)

# spokes de supervision, orchestrateur <-> agents
for aid, _, _, _ in AGENTS:
    label = "Vidéo source" if aid == "a1" else None
    lien(f"e-orch-{aid}", "orchestrateur", aid, label, "#9ca3af")

# boucle de feedback de l'agent 5 vers les agents 1, 3 et 4
for cible in ("a1", "a3", "a4"):
    lien(f"e-feedback-{cible}", "a5", cible, "Feedback de correction", "#8b5cf6")

canvas = {"nodes": nodes, "edges": list(edges.values())}

racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chemin = os.path.join(racine, SORTIE)
with open(chemin, "w", encoding="utf-8") as f:
    json.dump(canvas, f, ensure_ascii=False, indent=2)
print(f"{chemin} : {len(nodes)} cartes, {len(canvas['edges'])} liens")
