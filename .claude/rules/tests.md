# Règles tests automatisés

## Activation

Conditionnel — activé si choix Phase 1 (Q5) = `Oui`.

Si activé :
- Dossier `tests/` obligatoire dans le contrat architectural (Phase 4).
- Lot dédié supplémentaire en Phase 5 (Petit : 4 lots · Moyen/Grand : 5 lots).
- `requirements-dev.txt` obligatoire.

Si désactivé :
- Aucun dossier `tests/`, aucun lot supplémentaire.
- Nombre de lots inchangé (Petit : 3 · Moyen/Grand : 4).

---

## Stack non négociable

- `pytest >= 8.0`
- `pytest-qt >= 4.4` (smoke tests Views)
- `unittest.mock` (stdlib) pour les mocks — zéro framework externe

---

## Structure obligatoire

```
tests/
├── __init__.py
├── conftest.py                          # Fixtures partagées (qapp via pytest-qt auto)
├── test_helpers.py                      # 1 fichier par module utils
├── models/
│   ├── __init__.py
│   ├── test_exceptions.py               # Smoke isinstance
│   └── test_[entite]_model.py           # 1 par modèle
├── controllers/
│   ├── __init__.py
│   └── test_[entite]_controller.py      # 1 par controller (model mocké)
└── views/
    ├── __init__.py
    └── test_[entite]_view.py            # Smoke uniquement
```

---

## Conventions

- Nommage fichier : `test_[module].py` pour tester `[module].py`.
- Nommage fonction : `test_[comportement]` en français explicite.
  Exemple : `test_validation_email_invalide_leve_validation_error`.
- Une classe `Test[Classe]` par classe testée, sinon fonctions plates.
- `@pytest.mark.parametrize` uniquement si ≥ 3 cas similaires.
- Aucun `assert True`, aucun test vide, aucun `pass`.
- Aucun `time.sleep` — utiliser `qtbot.wait`, `qtbot.waitSignal` ou mocks.
- Aucun accès réseau, aucun accès DB de production — fixtures isolées.

---

## Couverture cible par couche

| Couche                  | Cible                          | Quoi tester                                                |
| ----------------------- | ------------------------------ | ---------------------------------------------------------- |
| `models/`               | Logique métier complète        | Méthodes publiques, exceptions levées, edge cases          |
| `models/exceptions.py`  | Smoke isinstance               | Chaque exception hérite bien d'`Exception`                 |
| `controllers/`          | Wiring + try/except            | Model mocké, `view.show_toast` appelé avec bon type        |
| `utils/helpers.py`      | 100% lignes                    | Toutes branches des fonctions pures                        |
| `views/`                | Smoke uniquement               | Instanciation sans crash + `objectName` présents           |

---

## Pattern test controller (obligatoire)

```python
from unittest.mock import Mock
from controllers.client_controller import ClientController
from models.exceptions import ValidationError, DatabaseError


def test_save_validation_error_emet_toast_warning():
    view = Mock()
    model = Mock()
    model.save.side_effect = ValidationError("Email invalide")
    controller = ClientController(view, model)

    controller.save({"email": "bad"})

    view.show_toast.assert_called_once_with("warning", "Email invalide")


def test_save_database_error_emet_toast_danger():
    view = Mock()
    model = Mock()
    model.save.side_effect = DatabaseError("Connexion perdue")
    controller = ClientController(view, model)

    controller.save({"email": "ok@test.fr"})

    view.show_toast.assert_called_once()
    args = view.show_toast.call_args.args
    assert args[0] == "danger"
```

---

## Pattern smoke test view (obligatoire)

```python
import pytest
from PyQt6.QtWidgets import QPushButton
from views.client_view import ClientView


def test_client_view_instanciation(qtbot):
    view = ClientView()
    qtbot.addWidget(view)
    assert view.objectName() == "client_view"


def test_client_view_contient_bouton_primaire(qtbot):
    view = ClientView()
    qtbot.addWidget(view)
    btn = view.findChild(QPushButton, "btn_primary")
    assert btn is not None
```

---

## conftest.py — structure minimale

```python
"""Fixtures partagées pour la suite de tests."""

# qapp est fournie automatiquement par pytest-qt — ne pas redéfinir.
# Ajouter ici uniquement les fixtures projet : db temporaire, model mocké, etc.

import pytest


@pytest.fixture
def empty_model():
    """Modèle vide réutilisable, à mocker dans les tests controllers."""
    from unittest.mock import Mock
    return Mock()
```

---

## Lancement

```bash
pytest                              # Tous les tests
pytest tests/models/                # Une couche
pytest -k validation                # Filtre par nom
pytest -v                           # Verbeux
pytest --tb=short                   # Traceback court
```

---

## Vérification d'intégrité du lot tests

1. Chaque module source (`models/`, `controllers/`, `views/`, `utils/`) a son fichier test correspondant.
2. `pytest` exit code 0 — tous les tests passent.
3. Aucun `assert True`, aucun test vide.
4. Aucun `time.sleep`.
5. Aucun accès réseau ou DB de production.
6. `requirements-dev.txt` présent et à jour.
