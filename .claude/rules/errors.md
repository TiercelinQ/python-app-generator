# Protocole gestion des erreurs

## Principe de séparation

- **Model** : lève des exceptions métier explicites (classes dans `models/exceptions.py`).
- **Controller** : intercepte via `try/except`. Ne propage jamais d'exception vers la View.
- **View** : expose `show_toast(type, message, description=None)`. Ne gère aucune logique d'erreur.

## models/exceptions.py — structure obligatoire

```python
# models/exceptions.py
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

## Pattern controller — obligatoire

```python
# controller — pattern obligatoire
try:
    result = self.model.save(data)
except ValidationError as e:
    self.view.show_toast("warning", str(e))
except RecordNotFoundError as e:
    self.view.show_toast("danger", str(e))
except DatabaseError as e:
    self.view.show_toast("danger", "Erreur base de données", str(e))
```

## show_toast — signature obligatoire dans toute vue principale

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

## Interdictions

- Zéro `QMessageBox` pour erreurs métier.
- Zéro bandeau inline.
- Zéro exception propagée hors du controller.
- Zéro `except Exception` attrapant tout sans re-raise.

## Toasts — durées (layout.md)

| Type      | Durée      | Fermeture manuelle  |
| --------- | ---------- | ------------------- |
| `success` | 4s         | Non                 |
| `info`    | 4s         | Non                 |
| `warning` | 6s         | Oui (×)             |
| `danger`  | persistant | Oui (×) obligatoire |
