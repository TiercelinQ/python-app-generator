---
description: Génère ou régénère le fichier README.md d'un projet Python/PyQt6 existant
             en analysant le code source. Invoquer depuis la racine du projet cible.
model: claude-sonnet-4-6
---

## Analyse du projet

!`find . -type f -name "*.py" | grep -v "__pycache__" | grep -v ".venv" | sort`
!`cat config.py 2>/dev/null || echo "config.py introuvable"`
!`cat requirements.txt 2>/dev/null || echo "requirements.txt introuvable"`
!`cat main.py 2>/dev/null || echo "main.py introuvable"`

## Instructions

Sur la base de l'analyse ci-dessus, générer un fichier `README.md` à la racine du projet :

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

## Couleur primaire
[Déduite de PRIMARY_600 / PRIMARY_400 dans config.py — sinon "Slate Blue #4F46E5 / #818CF8"]
```

Écrire le fichier directement :

```bash
cat > README.md << 'EOF'
[contenu généré]
EOF
```

Confirmer avec :
`README.md généré à la racine du projet.`