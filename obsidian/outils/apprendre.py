#!/usr/bin/env python3
"""Mémoire et apprentissage des agents.

Chaque agent a un fichier de mémoire dans `memoire/agent-N.json`.
Ce script est le seul à y écrire, puis il réécrit les zones marquées
de la fiche `agents/agent-N-*.md` et le `Tableau de bord.md`.

Tout ce qui est HORS des marqueurs <!-- ZONE:DEBUT --> … <!-- ZONE:FIN -->
reste à toi : le script n'y touche jamais.

Boucle d'apprentissage
----------------------
1. l'agent tourne                     → `succes  --agent 3`
2. l'agent se plante                  → `lecon   --agent 3 --erreur "…" --regle "…"`
3. une règle grave entre dans le prompt de l'agent (gravité `bloquant`)
4. la série repart de zéro ; l'agent est « autonome » quand il atteint son objectif

Exemples
--------
    python3 outils/apprendre.py lecon --agent 3 \
        --erreur "clip coupé au milieu du mot « exactement » à 00:04:12" \
        --regle "vérifier la frontière de mot sur les 5 dernières frames" \
        --gravite bloquant --source agent-5

    python3 outils/apprendre.py succes --agent 3 --fois 2
    python3 outils/apprendre.py etat
"""

import argparse
import datetime
import glob
import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_MEMOIRE = os.path.join(RACINE, "memoire")
DOSSIER_AGENTS = os.path.join(RACINE, "agents")
TABLEAU = os.path.join(RACINE, "Tableau de bord.md")

GRAVITES = ("bloquant", "mineur")
STATUTS = [
    # (part de l'objectif atteinte, libellé, jauge)
    (1.00, "autonome", "🟩"),
    (0.70, "presque", "🟨"),
    (0.30, "en progrès", "🟧"),
    (0.00, "en rodage", "🟥"),
]


# --------------------------------------------------------------------------
# lecture / écriture de la mémoire
# --------------------------------------------------------------------------

def chemin_memoire(n):
    return os.path.join(DOSSIER_MEMOIRE, f"agent-{n}.json")


def charger(n):
    chemin = chemin_memoire(n)
    if not os.path.exists(chemin):
        sys.exit(f"Pas de mémoire pour l'agent {n} ({chemin} est introuvable).")
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def enregistrer(m):
    with open(chemin_memoire(m["agent"]), "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
        f.write("\n")


def tous():
    fichiers = sorted(glob.glob(os.path.join(DOSSIER_MEMOIRE, "agent-*.json")))
    return [json.load(open(f, encoding="utf-8")) for f in fichiers]


def fiche_de(n):
    trouves = glob.glob(os.path.join(DOSSIER_AGENTS, f"agent-{n}-*.md"))
    return trouves[0] if trouves else None


def aujourdhui():
    return datetime.date.today().isoformat()


# --------------------------------------------------------------------------
# statut d'autonomie
# --------------------------------------------------------------------------

def statut(m):
    a = m["autonomie"]
    objectif = max(1, a["objectif"])
    part = a["serie"] / objectif
    for seuil, libelle, jauge in STATUTS:
        if part >= seuil:
            return libelle, jauge
    return "en rodage", "🟥"


def jauge(m, largeur=10):
    a = m["autonomie"]
    objectif = max(1, a["objectif"])
    pleins = min(largeur, round(largeur * a["serie"] / objectif))
    return "▰" * pleins + "▱" * (largeur - pleins)


# --------------------------------------------------------------------------
# rendu des zones marquées
# --------------------------------------------------------------------------

def remplacer_zone(texte, zone, contenu):
    """Réécrit ce qui est entre <!-- zone:DEBUT --> et <!-- zone:FIN -->."""
    debut = f"<!-- {zone}:DEBUT -->"
    fin = f"<!-- {zone}:FIN -->"
    motif = re.compile(
        re.escape(debut) + r".*?" + re.escape(fin), re.DOTALL)
    if not motif.search(texte):
        raise SystemExit(f"Zone {zone} absente de la fiche : marqueurs perdus ?")
    return motif.sub(f"{debut}\n{contenu.rstrip()}\n{fin}", texte)


def rendu_memoire(m):
    lignes = []

    regles = [l for l in m["lecons"] if l["regle"]]
    lignes.append("### Règles apprises")
    if regles:
        for l in regles:
            marque = " ⛔" if l["gravite"] == "bloquant" else ""
            lignes.append(f"- `{l['date']}` {l['regle']}{marque}")
    else:
        lignes.append("- *(aucune pour l'instant)*")

    erreurs = [l for l in m["lecons"] if l["erreur"]]
    lignes.append("")
    lignes.append("### Erreurs passées")
    if erreurs:
        for l in erreurs:
            source = f" — signalé par {l['source']}" if l.get("source") else ""
            lignes.append(f"- `{l['date']}` {l['erreur']}{source}")
    else:
        lignes.append("- *(aucune pour l'instant)*")

    lignes.append("")
    lignes.append("### Améliorations appliquées")
    if m["ameliorations"]:
        for a in m["ameliorations"]:
            lignes.append(f"- `{a['date']}` {a['texte']}")
    else:
        lignes.append("- *(aucune pour l'instant)*")

    lignes.append("")
    lignes.append("### Notes personnelles")
    lignes.append(m["notes"] or "*(rien noté)*")

    return "\n".join(lignes)


def rendu_autonomie(m):
    a = m["autonomie"]
    libelle, icone = statut(m)
    return (
        f"{icone} **{libelle}** — {jauge(m)} "
        f"{a['serie']} / {a['objectif']} exécutions propres d'affilée\n\n"
        f"| Exécutions | Incidents | Meilleure série | Objectif |\n"
        f"|---|---|---|---|\n"
        f"| {a['executions']} | {a['incidents']} | {a['meilleure_serie']} | {a['objectif']} |\n\n"
        f"> Un incident remet la série à zéro. L'agent est considéré comme "
        f"autonome quand il atteint son objectif sans faute."
    )


def rendu_prompt(m):
    """Le prompt de base, plus les règles graves apprises depuis."""
    lignes = list(m["prompt_base"])
    graves = [l for l in m["lecons"] if l["gravite"] == "bloquant" and l["regle"]]
    if graves:
        lignes.append("")
        lignes.append("# Règles apprises — ajoutées automatiquement, ne pas retirer à la main")
        for l in graves:
            lignes.append(f"- {l['regle']}")
    corps = "\n".join(lignes)
    return "```prompt\n" + corps + "\n```"


def ecrire_fiche(m):
    chemin = fiche_de(m["agent"])
    if not chemin:
        print(f"  ! fiche introuvable pour l'agent {m['agent']}")
        return
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    texte = remplacer_zone(texte, "AUTONOMIE", rendu_autonomie(m))
    texte = remplacer_zone(texte, "MEMOIRE", rendu_memoire(m))
    texte = remplacer_zone(texte, "PROMPT", rendu_prompt(m))
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)


def ecrire_tableau(memoires):
    lignes = [
        "---",
        "tags: [tableau-de-bord, pipeline-shorts]",
        "---",
        "",
        "# 📊 Tableau de bord — autonomie des agents",
        "",
        f"*Mis à jour le {aujourdhui()}.* Ce fichier est régénéré automatiquement :",
        "ne l'écris pas à la main, il serait écrasé.",
        "",
        "| Agent | Statut | Progression | Série | Incidents | Dernière leçon |",
        "|---|---|---|---|---|---|",
    ]
    for m in memoires:
        libelle, icone = statut(m)
        derniere = m["lecons"][-1]["date"] if m["lecons"] else "—"
        fiche = fiche_de(m["agent"])
        lien = os.path.splitext(os.path.basename(fiche))[0] if fiche else ""
        lignes.append(
            f"| [[{lien}|{m['agent']} — {m['nom']}]] "
            f"| {icone} {libelle} "
            f"| {jauge(m)} "
            f"| {m['autonomie']['serie']} / {m['autonomie']['objectif']} "
            f"| {m['autonomie']['incidents']} "
            f"| {derniere} |"
        )

    autonomes = sum(1 for m in memoires if statut(m)[0] == "autonome")
    lignes += [
        "",
        f"**{autonomes} agent(s) sur {len(memoires)} au niveau autonome.**",
        "",
        "## Comment ça bouge",
        "",
        "| Ce qui arrive | La commande | L'effet |",
        "|---|---|---|",
        "| L'agent a bien travaillé | `succes --agent N` | la série avance |",
        "| L'agent s'est trompé | `lecon --agent N --erreur … --regle …` | la série repart de zéro, la règle est écrite |",
        "| La règle est grave | `--gravite bloquant` | la règle entre dans le prompt de l'agent |",
        "",
        "Les fiches sont dans `agents/`, la mémoire brute dans `memoire/`.",
    ]
    with open(TABLEAU, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")


def tout_rendre():
    memoires = tous()
    for m in memoires:
        ecrire_fiche(m)
    ecrire_tableau(memoires)
    return memoires


# --------------------------------------------------------------------------
# commandes
# --------------------------------------------------------------------------

def cmd_lecon(args):
    m = charger(args.agent)
    m["lecons"].append({
        "date": args.date or aujourdhui(),
        "erreur": args.erreur or "",
        "regle": args.regle,
        "gravite": args.gravite,
        "source": args.source or "",
    })
    a = m["autonomie"]
    if args.erreur:
        a["incidents"] += 1
        a["serie"] = 0
    enregistrer(m)
    tout_rendre()
    libelle, icone = statut(m)
    print(f"Agent {m['agent']} — leçon enregistrée.")
    if args.gravite == "bloquant":
        print("  → règle ajoutée à son prompt : il l'appliquera désormais.")
    if args.erreur:
        print(f"  → série remise à zéro. Statut : {icone} {libelle}.")


def cmd_succes(args):
    m = charger(args.agent)
    a = m["autonomie"]
    a["executions"] += args.fois
    a["serie"] += args.fois
    a["meilleure_serie"] = max(a["meilleure_serie"], a["serie"])
    enregistrer(m)
    tout_rendre()
    libelle, icone = statut(m)
    print(f"Agent {m['agent']} — {a['serie']} / {a['objectif']} "
          f"exécutions propres. Statut : {icone} {libelle}.")
    if libelle == "autonome":
        print("  → objectif atteint. Cet agent tourne seul.")


def cmd_amelioration(args):
    m = charger(args.agent)
    m["ameliorations"].append({"date": aujourdhui(), "texte": args.texte})
    enregistrer(m)
    tout_rendre()
    print(f"Agent {m['agent']} — amélioration notée.")


def cmd_note(args):
    m = charger(args.agent)
    m["notes"] = args.texte
    enregistrer(m)
    tout_rendre()
    print(f"Agent {m['agent']} — note mise à jour.")


def cmd_objectif(args):
    m = charger(args.agent)
    m["autonomie"]["objectif"] = args.valeur
    enregistrer(m)
    tout_rendre()
    print(f"Agent {m['agent']} — objectif porté à {args.valeur}.")


def cmd_fiches(_args):
    memoires = tout_rendre()
    print(f"{len(memoires)} fiches et le tableau de bord régénérés.")


def cmd_etat(_args):
    memoires = tous()
    if not memoires:
        sys.exit("Aucune mémoire trouvée dans memoire/.")
    largeur = max(len(m["nom"]) for m in memoires)
    print()
    for m in memoires:
        libelle, icone = statut(m)
        a = m["autonomie"]
        print(f"  {icone} Agent {m['agent']}  {m['nom']:<{largeur}}  "
              f"{jauge(m)}  {a['serie']:>2} / {a['objectif']:<2}  "
              f"{libelle:<11} {a['incidents']} incident(s)")
    autonomes = sum(1 for m in memoires if statut(m)[0] == "autonome")
    print(f"\n  {autonomes} / {len(memoires)} agents autonomes.\n")


def principal():
    p = argparse.ArgumentParser(
        description="Mémoire et apprentissage des agents.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sous = p.add_subparsers(dest="commande", required=True)

    s = sous.add_parser("lecon", help="l'agent s'est trompé, ou a appris une règle")
    s.add_argument("--agent", type=int, required=True)
    s.add_argument("--regle", required=True, help="la règle à retenir")
    s.add_argument("--erreur", help="ce qui s'est mal passé (si incident)")
    s.add_argument("--gravite", choices=GRAVITES, default="mineur")
    s.add_argument("--source", help="qui l'a signalé : agent-5, humain, plateforme…")
    s.add_argument("--date", help="par défaut : aujourd'hui")
    s.set_defaults(fn=cmd_lecon)

    s = sous.add_parser("succes", help="l'agent a bien travaillé")
    s.add_argument("--agent", type=int, required=True)
    s.add_argument("--fois", type=int, default=1)
    s.set_defaults(fn=cmd_succes)

    s = sous.add_parser("amelioration", help="noter une amélioration appliquée")
    s.add_argument("--agent", type=int, required=True)
    s.add_argument("--texte", required=True)
    s.set_defaults(fn=cmd_amelioration)

    s = sous.add_parser("note", help="remplacer les notes personnelles")
    s.add_argument("--agent", type=int, required=True)
    s.add_argument("--texte", required=True)
    s.set_defaults(fn=cmd_note)

    s = sous.add_parser("objectif", help="changer le seuil d'autonomie")
    s.add_argument("--agent", type=int, required=True)
    s.add_argument("--valeur", type=int, required=True)
    s.set_defaults(fn=cmd_objectif)

    s = sous.add_parser("fiches", help="régénérer fiches et tableau de bord")
    s.set_defaults(fn=cmd_fiches)

    s = sous.add_parser("etat", help="afficher l'autonomie des 6 agents")
    s.set_defaults(fn=cmd_etat)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    principal()
