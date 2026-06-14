---
name: phase4-contrat
description: Phase 4 of the development cycle — architectural contract (full tree, role of each file, tokens → QSS table, source→test mapping), written to the contract spec and locked after validation.
model: sonnet
---

# /phase4-contrat — Architectural contract

## Role
Software architect — design the locked structure the whole build will follow.

## Goal
Produce a complete, unambiguous architectural contract that freezes the file tree, QSS mapping, and (if tests) the source→test mapping.

## Deliverable
`docs/specs/04-contrat.md` (written in French) — the locked source of truth + on-screen contract.

---

At start: read `design-system.md`, `layout.md` (no longer auto-imported), `rules/mvc.md` (tree, batches) and `rules/qss.md` (tokens → QSS). Read `docs/specs/01-cadrage.md` through `03-layout.md` for the validated decisions.

Present the complete project tree with the role of each file, then the QSS token table. Output format (in French):

```
## Contrat architectural — [NOM_APP]

### Arborescence

[nom_app]/
├── main.py                        # Point d'entrée — QApplication, MainWindow, logger, migrations, excepthook
├── config.py                      # Constantes globales, ICON_COLORS, PRIMARY_*
├── requirements.txt
├── pyproject.toml                 # Config ruff, mypy, pytest
├── docs/specs/                    # Specs de génération (FR) : 01-cadrage … 04-contrat
├── preferences.json               # Racine projet — généré au 1er lancement (si Q3=Oui)
├── logs/                          # Créé automatiquement par utils/logger.py
├── models/
│   ├── __init__.py
│   ├── exceptions.py              # Exceptions métier nommées
│   ├── db.py                      # Point d'accès DB unique (si DB ≠ aucune)
│   ├── migrations.py              # Migrations versionnées (si DB ≠ aucune)
│   └── [entite]_model.py          # [rôle]
├── views/
│   ├── __init__.py
│   ├── main_window.py             # Fenêtre principale, topbar, layout global, install_excepthook
│   ├── toast_manager.py           # Toasts (position, animation, file)
│   └── [entite]_view.py           # [rôle]
├── controllers/
│   ├── __init__.py
│   └── [entite]_controller.py     # [rôle]
├── utils/
│   ├── helpers.py                 # Fonctions pures (formatage, JSON, validation)
│   └── logger.py                  # Configuration logging (@rules/logging.md)
└── resources/
    ├── styles_light.qss           # Thème clair — tous tokens design-system.md
    ├── styles_dark.qss            # Thème sombre — tous tokens design-system.md
    └── i18n/                      # Si i18n activée (@rules/i18n.md) : app_{fr,en}.{ts,qm}

# Si tests activés en Phase 1 :
tests/                             # Miroir de la structure source (@rules/tests.md)
requirements-dev.txt               # pytest>=8.0.0, pytest-qt>=4.4.0

### Tableau tokens → règles QSS

| Token design-system.md | Valeur clair | Valeur sombre | Règle QSS cible |
| ----------------------- | ------------ | ------------- | --------------- |
| bg                      | #FFFFFF      | #111827       | QMainWindow, #main_content, #topbar |
| primary-600             | #4F46E5      | —             | QTabBar::tab:selected, #btn_primary |
| …                       | …            | …             | …               |

### Mapping sources → tests (si tests activés)

| Module source                        | Fichier test                                  |
| ------------------------------------ | --------------------------------------------- |
| `models/[entite]_model.py`           | `tests/models/test_[entite]_model.py`         |
| `controllers/[entite]_controller.py` | `tests/controllers/test_[entite]_controller.py` |
| `views/[entite]_view.py`             | `tests/views/test_[entite]_view.py` (smoke)   |
| `utils/helpers.py`                   | `tests/test_helpers.py`                       |
```

End with:

```
→ Ce contrat est verrouillé après validation.
  Tout écart ultérieur (fusion, scission, renommage, ajout, suppression) impose :
  1. Arrêt.
  2. Déclaration de l'écart + justification.
  3. Validation avant reprise.

  Confirmer pour démarrer la Phase 5.
```

**Blocking rule**: do not deliver Batch 1 until validation is explicit.

## Write the spec

Once validated, write the full contract to `docs/specs/04-contrat.md` (in French). This file is the **locked source of truth** re-read by `/phase5-developpement`, `/charger-projet`, `/contrat`, `/feature-add`, and `/refactor`.

Chain to `/phase5-developpement` after validation.
