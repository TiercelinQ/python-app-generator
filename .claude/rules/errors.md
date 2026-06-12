# Protocole gestion des erreurs

## Principe de séparation

- **Model** : lève des exceptions métier explicites (classes dans `models/exceptions.py`).
- **Controller** : intercepte via `try/except`. Ne propage jamais d'exception vers la View.
- **View** : expose `show_toast(type, message, description=None)`. Ne gère aucune logique d'erreur.

---

## `models/exceptions.py` — structure obligatoire

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

Jamais `raise Exception("message")` générique dans les models.

---

## Pattern controller — obligatoire

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

Notification d'information (action neutre, pas une erreur) :

```python
self.view.show_toast("info", "Export démarré", "Fichier généré dans 5s")
```

---

## `show_toast` — signature obligatoire dans toute vue principale

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

## Mapping exception → toast (référence)

| Exception métier         | Type toast | Description optionnelle conseillée |
| ------------------------ | ---------- | ---------------------------------- |
| `ValidationError`        | warning    | Détail du champ invalide           |
| `RecordNotFoundError`    | danger     | —                                  |
| `DatabaseError`          | danger     | `str(e)` (technique)               |
| `FileError`              | danger     | Chemin du fichier                  |
| Succès métier            | success    | —                                  |
| Information non bloquante| info       | —                                  |

---

## Gestion des exceptions non capturées — `sys.excepthook`

Tout crash non géré dans le thread Qt principal doit :
1. Être loggé avec stacktrace complète.
2. Afficher un toast `danger` à l'utilisateur.
3. Ne pas écrire sur stdout/stderr en mode `--windowed`.

Installation dans `main.py` (obligatoire) :

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

Appel :

```python
window = MainWindow()
install_excepthook(window)
window.show()
```

---

## Interdictions

- Zéro `QMessageBox` pour erreurs métier.
- Zéro bandeau inline.
- Zéro exception propagée hors du controller.
- Zéro `except Exception` attrapant tout sans re-raise — sauf dans l'`excepthook`.
- Zéro `print(traceback)` — utiliser `logger.exception(...)`.

---

## Toasts — durées (layout.md)

| Type      | Durée      | Fermeture manuelle  |
| --------- | ---------- | ------------------- |
| `success` | 4s         | Non                 |
| `info`    | 4s         | Non                 |
| `warning` | 6s         | Oui (×)             |
| `danger`  | persistant | Oui (×) obligatoire |
