# Automated tests rules

## Activation

Conditional — enabled if Phase 1 tests = `Yes`.

If enabled:
- `tests/` folder mandatory in the architectural contract (Phase 4).
- Dedicated extra batch in Phase 5 (Small: 4 batches · Medium/Large: 5 batches).
- `requirements-dev.txt` mandatory.

If disabled:
- No `tests/` folder, no extra batch.
- Batch count unchanged (Small: 3 · Medium/Large: 4).

---

## Non-negotiable stack

- `pytest >= 8.0`
- `pytest-qt >= 4.4` (View smoke tests)
- `unittest.mock` (stdlib) for mocks — zero external framework

---

## Mandatory structure

```
tests/
├── __init__.py
├── conftest.py                          # Shared fixtures (qapp via pytest-qt auto)
├── test_helpers.py                      # 1 file per utils module
├── models/
│   ├── __init__.py
│   ├── test_exceptions.py               # isinstance smoke
│   └── test_[entity]_model.py           # 1 per model
├── controllers/
│   ├── __init__.py
│   └── test_[entity]_controller.py      # 1 per controller (mocked model)
└── views/
    ├── __init__.py
    └── test_[entity]_view.py            # Smoke only
```

---

## Conventions

- File naming: `test_[module].py` to test `[module].py`.
- Function naming: `test_[behavior]` in explicit French — always French, independent of the user's interface language.
  Example: `test_validation_email_invalide_leve_validation_error`.
- One `Test[Class]` class per tested class, otherwise flat functions.
- `@pytest.mark.parametrize` only for ≥ 3 similar cases.
- No `assert True`, no empty test, no `pass`.
- No `time.sleep` — use `qtbot.wait`, `qtbot.waitSignal`, or mocks.
- No network access, no production DB access — isolated fixtures.

---

## Target coverage per layer

| Layer                   | Target                         | What to test                                               |
| ----------------------- | ------------------------------ | ---------------------------------------------------------- |
| `models/`               | Full business logic            | Public methods, raised exceptions, edge cases              |
| `models/exceptions.py`  | isinstance smoke               | Each exception properly inherits `Exception`               |
| `controllers/`          | Wiring + try/except            | Mocked model, `view.show_toast` called with the right type |
| `utils/helpers.py`      | 100% lines                     | All branches of the pure functions                         |
| `views/`                | Smoke only                     | Instantiation without crash + `objectName` present         |

---

## Controller test pattern (mandatory)

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

## View smoke test pattern (mandatory)

```python
import pytest
from PySide6.QtWidgets import QPushButton
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

## conftest.py — minimal structure

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

## Running

```bash
pytest                              # All tests
pytest tests/models/                # One layer
pytest -k validation                # Filter by name
pytest -v                           # Verbose
pytest --tb=short                   # Short traceback
```

---

## Anti-patterns — what NOT to do

- **Do not** write `assert True`, an empty test, or a `pass` body.
- **Do not** use `time.sleep` — use `qtbot.wait` / `qtbot.waitSignal` / mocks.
- **Do not** hit the network or a production DB — isolated fixtures only.
- **Do not** redefine the `qapp` fixture — pytest-qt provides it.
- **Do not** test a controller without mocking its model.
- **Do not** go beyond smoke for views (instantiation + `objectName` + key widgets via `findChild`).
- **Do not** create a test suite when Phase 1 tests = No (and `/python-run-tests` never scaffolds one unasked).

## Integrity verification

Detailed in `@rules/verification.md`. Key points: each source module has its matching test file (Phase 4 mapping); `pytest` exit code 0; `requirements-dev.txt` present.
