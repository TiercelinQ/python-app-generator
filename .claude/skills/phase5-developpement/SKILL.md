---
description: Phase 5 du cycle de développement — livraison du code par lots.
             Invoquer après validation du contrat architectural (Phase 4).
             Aussi invoquer pour chaque lot suivant dès la fin du lot précédent.
model: claude-sonnet-4-6
---

## Instructions — Phase 5 : Développement par lots

### Avant chaque lot

Annoncer : `📦 Lot N/[total] — [contenu]`

Livrer chaque fichier en bloc complet et autonome dans un bloc de code nommé.

### Après chaque lot (sauf le dernier)

Enchaîner immédiatement sur le lot suivant sans attendre de confirmation.

### Dernier lot — fichiers obligatoires

**1. Instructions d'installation** — inclure après `requirements.txt` :

```
## Installation

# 1. Créer l'environnement virtuel
python -m venv .venv

# 2. Activer (Windows)
.venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python main.py
```

**2. README.md** — générer à la racine du projet :

```markdown
# [NOM_APP] — v[VERSION]

## Objectif
[Description synthétique issue de la Phase 2]

## Fonctionnalités
- [Liste des fonctionnalités retenues — Phase 2]

## Hors périmètre
- [Liste — Phase 2]

## Stack technique
- OS : Windows
- Framework : PyQt6
- Python : 3.10+
- Icônes : qtawesome
- DB : [valeur]
- i18n : [Oui/Non]

## Architecture
[Arborescence du contrat — Phase 4 avec rôle de chaque fichier]

## Installation
[Reprendre les instructions ci-dessus]

## Couleur primaire
[Nom + hex clair + hex sombre]
```

---

## Vérification d'intégrité (silencieuse — signalée si écart)

**Chaque lot :**
1. Syntaxe Python valide.
2. Imports : tous utilisés, aucun manquant, séparation MVC respectée.
3. Responsabilités MVC respectées.
4. Zéro `# TODO`, zéro `pass` injustifié.
5. Python 3.10+ · PyQt6 stable · zéro API PyQt5.
6. Conformité `design-system.md` et `layout.md`.

**Dernier lot uniquement — cross-fichiers :**
7. Tous imports inter-couches résolus.
8. Signaux/slots cohérents.
9. Contrat architectural respecté.
10. Zéro valeur visuelle en dur dans Python.
11. README.md généré et complet.

---

## Ajustements post-livraison

Correction isolée sur le fichier concerné + ses dépendances directes.
Livraison du fichier complet corrigé (jamais de diff partiel).

## Résolution d'anomalie

Dès que la solution définitive est identifiée et livrée, produire :

```
Anomalie résolue. Éléments à retirer des tentatives précédentes :

Fichier [nom] :
- [ligne / bloc / import / objectName à supprimer]
```