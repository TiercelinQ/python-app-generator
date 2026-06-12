# Règles MVC strictes

## Séparation des responsabilités

- `models/` : logique métier, accès données. Jamais PyQt6 sauf `QObject`/`pyqtSignal`.
- `views/` : widgets PyQt6 uniquement. Aucune logique métier. Émet des signaux.
- `controllers/` : connecte signaux View → Model. Aucune mise en page.
- Imports unidirectionnels : Controller → Model + View. Jamais Model → View.
- Une entité = un fichier. Constantes dans `config.py`.

## Structure obligatoire

```
models/
├── __init__.py
├── exceptions.py          # Exceptions métier nommées
└── [entite]_model.py      # Un fichier par entité

views/
├── __init__.py
├── main_window.py         # Fenêtre principale (topbar, layout global)
├── toast_manager.py       # Système de toasts
└── [entite]_view.py       # Un fichier par vue

controllers/
├── __init__.py
└── [entite]_controller.py # Un fichier par entité

utils/
└── helpers.py             # Fonctions pures uniquement — zéro PyQt6, zéro logique métier

tests/                     # Si tests activés en Phase 1 — voir @rules/tests.md
├── __init__.py
├── conftest.py
├── test_helpers.py
├── models/
├── controllers/
└── views/
```

## utils/helpers.py — contenu autorisé uniquement

- Formatage de dates, nombres, chaînes.
- Validation de données (email, numérique…).
- Lecture/écriture fichiers JSON (préférences).
- Fonctions de conversion génériques.

## Vérification d'intégrité par lot (silencieuse — signalée si écart)

Chaque lot :

1. Syntaxe Python valide.
2. Imports : tous utilisés, aucun manquant, séparation MVC respectée.
3. Responsabilités MVC respectées.
4. Zéro `# TODO`, zéro `pass` injustifié.
5. Python 3.10+ · PyQt6 stable · zéro API PyQt5.
6. Conformité `design-system.md` et `layout.md`.

Dernier lot uniquement — cross-fichiers :
7. Tous imports inter-couches résolus.
8. Signaux/slots cohérents.
9. Contrat architectural respecté.
10. Zéro valeur visuelle en dur dans Python.
11. README.md généré et complet.

Lot tests uniquement (si activé) :
12. Chaque module source a son fichier test correspondant.
13. `pytest` exit code 0 — tous les tests passent.

## Livraison par lots

### Sans tests (Phase 1 Q5 = Non)

**Petit projet (3 lots) :**

| Lot | Contenu                                                                          |
| --- | -------------------------------------------------------------------------------- |
| 1   | `config.py` + `models/` (incluant `db.py` et `migrations.py` si DB)              |
| 2   | `views/` + `controllers/`                                                        |
| 3   | `main.py` + `utils/` + `resources/styles_*.qss` + `requirements.txt` + `pyproject.toml` + instructions |

**Moyen / Grand projet (4 lots) :**

| Lot | Contenu                                                                          |
| --- | -------------------------------------------------------------------------------- |
| 1   | `config.py` + `models/` (incluant `db.py` et `migrations.py` si DB)              |
| 2   | `views/`                                                                         |
| 3   | `controllers/`                                                                   |
| 4   | `main.py` + `utils/` + `resources/styles_*.qss` + `requirements.txt` + `pyproject.toml` + instructions |

### Avec tests (Phase 1 Q5 = Oui)

**Petit projet (4 lots) :**

| Lot | Contenu                                                                          |
| --- | -------------------------------------------------------------------------------- |
| 1   | `config.py` + `models/`                                                          |
| 2   | `views/` + `controllers/`                                                        |
| 3   | `main.py` + `utils/` + `resources/styles_*.qss` + `requirements.txt` + `pyproject.toml` + instructions |
| 4   | `tests/` + `requirements-dev.txt` + instructions pytest                          |

**Moyen / Grand projet (5 lots) :**

| Lot | Contenu                                                                          |
| --- | -------------------------------------------------------------------------------- |
| 1   | `config.py` + `models/`                                                          |
| 2   | `views/`                                                                         |
| 3   | `controllers/`                                                                   |
| 4   | `main.py` + `utils/` + `resources/styles_*.qss` + `requirements.txt` + `pyproject.toml` + instructions |
| 5   | `tests/` + `requirements-dev.txt` + instructions pytest                          |

### Contenu du dossier `utils/`

- `utils/helpers.py` — fonctions pures (formatage, validation, JSON)
- `utils/logger.py` — configuration logging (voir `@rules/logging.md`)
- `utils/resource_path.py` — helper PyInstaller `sys._MEIPASS` (si packaging opt-in)

### Format

Format d'annonce : `📦 Lot N/[total] — [contenu]`
Chaque fichier livré en bloc complet et autonome.
**Enchaînement automatique** entre les lots — aucune confirmation demandée.
L'utilisateur peut interrompre à tout moment.
En cas d'anomalie détectée par l'utilisateur après un lot : invocation libre de toute commande de correction.

## Résolution d'anomalie — protocole nettoyage

Dès que la solution définitive est identifiée et livrée :

```
Anomalie résolue. Éléments à retirer des tentatives précédentes :

Fichier [nom] :
- [ligne / bloc / import / objectName à supprimer]
```

## Ajustements post-livraison

Correction isolée sur le fichier concerné + ses dépendances directes. Livraison du fichier complet corrigé.
