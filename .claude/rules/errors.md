# Error handling protocol

## Separation principle

- **Model**: raises explicit business exceptions (classes in `models/exceptions.py`).
- **Controller**: intercepts via `try/except`. Never propagates an exception to the View.
- **View**: exposes `show_toast(type, message, description=None)`. Handles no error logic.

---

## `models/exceptions.py` — mandatory structure

```python
class RecordNotFoundError(Exception):
    """Enregistrement introuvable."""

class DatabaseError(Exception):
    """Erreur d'accès base de données."""

class ValidationError(Exception):
    """Données invalides."""

class FileError(Exception):
    """Erreur lecture/écriture fichier."""
```

If the Salesforce CLI integration is on (Phase 1), `models/exceptions.py` also defines (raised by `models/sf_cli.py`, see `@rules/sf-cli.md`):

```python
class SfCliNotFoundError(Exception):
    """sf CLI introuvable ou non exécutable (PATH/SF_CLI_PATH, shim .cmd Windows)."""

class SfCommandError(Exception):
    """sf a retourné status != 0, expiré, ou une réponse illisible."""
```

Never a generic `raise Exception("message")` in the models.

---

## Controller pattern — mandatory

```python
import logging

from models.exceptions import ValidationError, RecordNotFoundError, DatabaseError

logger = logging.getLogger(__name__)


def save(self, data: dict) -> None:
    try:
        result = self.model.save(data)
    except ValidationError as e:
        self.view.show_toast("warning", str(e))
    except RecordNotFoundError as e:
        self.view.show_toast("danger", str(e))
    except DatabaseError as e:
        logger.exception("Erreur base de données lors de la sauvegarde")
        self.view.show_toast("danger", "Erreur base de données", str(e))
    else:
        self.view.show_toast("success", "Enregistrement sauvegardé")
```

Information notification (neutral action, not an error):

```python
self.view.show_toast("info", "Export démarré", "Fichier généré dans 5s")
```

---

## `show_toast` — mandatory signature in every main view

```python
def show_toast(self, type: str, message: str, description: str | None = None) -> None:
    """Affiche un toast de notification.

    Args:
        type: "success" | "info" | "warning" | "danger"
        message: Message principal (police medium sm).
        description: Description optionnelle (police normal xs, text-subtle).
    """
    self.toast_manager.show(type, message, description)
```

---

## Exception → toast mapping (reference)

| Business exception       | Toast type | Suggested optional description     |
| ------------------------ | ---------- | ---------------------------------- |
| `ValidationError`        | warning    | Invalid field detail               |
| `RecordNotFoundError`    | danger     | —                                  |
| `DatabaseError`          | danger     | `str(e)` (technical)               |
| `FileError`              | danger     | File path                          |
| `SfCliNotFoundError`     | danger     | install / `SF_CLI_PATH` hint       |
| `SfCommandError`         | danger     | `str(e)` (sf message)              |
| Business success         | success    | —                                  |
| Non-blocking information  | info       | —                                  |

---

## Uncaught exceptions — `sys.excepthook`

Any unhandled crash in the main Qt thread must:
1. Be logged with full stacktrace.
2. Show a `danger` toast to the user.
3. Not write to stdout/stderr in `--windowed` mode.

Installation in `main.py` (mandatory):

```python
import logging
import sys

logger = logging.getLogger(__name__)


def install_excepthook(main_window) -> None:
    """Installe un excepthook global qui logge + notifie via toast."""

    def hook(exc_type, exc_value, exc_tb):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_tb)
            return
        logger.critical(
            "Exception non capturée",
            exc_info=(exc_type, exc_value, exc_tb),
        )
        try:
            main_window.show_toast(
                "danger",
                "Erreur inattendue",
                f"{exc_type.__name__} : {exc_value}",
            )
        except Exception:
            logger.exception("Échec affichage toast d'erreur critique")

    sys.excepthook = hook
```

Call:

```python
window = MainWindow()
install_excepthook(window)
window.show()
```

---

## Toasts — durations (layout.md)

| Type      | Duration   | Manual dismiss      |
| --------- | ---------- | ------------------- |
| `success` | 4s         | No                  |
| `info`    | 4s         | No                  |
| `warning` | 6s         | Yes (×)             |
| `danger`  | persistent | Yes (×) mandatory   |

---

## Anti-patterns — what NOT to do

- **Do not** use `QMessageBox` for a business error — toasts only.
- **Do not** use an inline banner — toasts only.
- **Do not** propagate an exception out of the controller.
- **Do not** use `except Exception` that catches everything without re-raise — except in the `excepthook`.
- **Do not** `print(traceback)` — use `logger.exception(...)`.
- **Do not** `raise Exception("...")` generic in a model — define a named exception in `models/exceptions.py`.
- **Do not** build the user-facing message in the model — the controller decides the toast wording.
