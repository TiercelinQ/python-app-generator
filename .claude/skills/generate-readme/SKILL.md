---
description: Génère ou régénère le fichier README.md d'un projet Python/PyQt6 existant
             en analysant le code source. Invoquer depuis la racine du projet cible.
model: claude-sonnet-4-6
---

## Analyse du projet

Utiliser les outils natifs Claude Code (pas de commandes shell — compatible Windows) :

1. **Lister les fichiers Python** via l'outil `Glob` avec le pattern `**/*.py`
   (exclure `__pycache__/`, `.venv/`, `venv/`).
2. **Lire** `config.py` via l'outil `Read` (ignorer si absent).
3. **Lire** `requirements.txt` via `Read` (ignorer si absent).
4. **Lire** `main.py` via `Read` (ignorer si absent).
5. **Détecter `tests/`** via `Glob` avec le pattern `tests/**/*.py`
   (présent si au moins un fichier retourné).
6. **Lire** `requirements-dev.txt` via `Read` si présent.

## Instructions

Sur la base de l'analyse, générer un fichier `README.md` à la racine du projet via
l'outil `Write` (jamais via `cat`/heredoc — incompatible Windows) :

```markdown
# [NOM_APP] — v[VERSION]

## Objectif
[Déduit de config.py, main.py et de la structure générale]

## Fonctionnalités
- [Déduites des views/ et controllers/ présents]

## Stack technique
- OS : Windows
- Framework : PyQt6
- Python : 3.10+
- Icônes : qtawesome
- DB : [déduit de config.py ou models/]
- i18n : [Oui/Non — déduit de resources/i18n/ ou config.py]
- Tests : [Oui (pytest + pytest-qt) | Non — déduit de la présence de tests/]

## Architecture
[Arborescence réelle du projet avec rôle de chaque fichier]

## Installation

# 1. Créer l'environnement virtuel
python -m venv .venv

# 2. Activer (Windows)
.venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python main.py

## Tests
[Section incluse uniquement si tests/ détecté]

pip install -r requirements-dev.txt
pytest                     # tous les tests
pytest tests/models/       # une couche
pytest -v                  # verbeux

## Couleur primaire
[Déduite de PRIMARY_600 / PRIMARY_400 dans config.py — sinon "Slate Blue #4F46E5 / #818CF8"]
```

Écrire le fichier via l'outil `Write` (chemin : `README.md` à la racine).

Confirmer avec :
`README.md généré à la racine du projet.`
