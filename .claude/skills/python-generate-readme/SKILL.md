---
name: python-generate-readme
description: Generate or regenerate the README.md of an existing Python/PyQt6 project from its specs and source code. Invoke from the target project root.
model: sonnet
---

# /python-generate-readme — Generate the README.md

## Role
Technical writer — produce an accurate project README from specs + code.

## Goal
Write a README that reflects what was actually built.

## Deliverable
`README.md` at the project root.

---

Use the native Claude Code tools (no shell — Windows-compatible):

1. **Sources, in priority**: `docs/specs/*` (especially `04-architect.md`) for the intended structure, then the real code:
   - List Python files via `Glob` `**/*.py` (exclude `__pycache__/`, `.venv/`, `venv/`).
   - Read `config.py`, `requirements.txt`, `main.py` (ignore if absent).
   - Detect `tests/` via `Glob` `tests/**/*.py`; read `requirements-dev.txt` if present.
   - When specs and code disagree, the code is what shipped — describe the code and note the divergence.
2. Generate `README.md` at the root via `Write`:

```markdown
# [NOM_APP] — v[VERSION]

## Objectif
[Déduit de docs/specs, config.py, main.py et de la structure]

## Fonctionnalités
- [Déduites des views/ et controllers/ présents]

## Stack technique
- OS : Windows · Framework : PyQt6 · Python : 3.10+ · Icônes : qtawesome
- DB : [déduit de config.py ou models/]
- i18n : [Oui/Non — déduit de resources/i18n/ ou config.py]
- Tests : [Oui (pytest + pytest-qt) | Non — déduit de la présence de tests/]

## Architecture
[Arborescence réelle avec rôle de chaque fichier]

## Installation
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py

## Tests
[Section incluse uniquement si tests/ détecté]
pip install -r requirements-dev.txt
pytest

## Couleur primaire
[Déduite de PRIMARY_600 / PRIMARY_400 dans config.py — sinon "Steel Blue #4682B4 / #5A9FD4"]
```

3. Write the file via `Write` (never `cat`/heredoc — Windows-incompatible).
4. If anything is undeterminable from specs + code: ask grouped questions (single block, French) before writing.

Confirm with: `README.md généré à la racine du projet.`
