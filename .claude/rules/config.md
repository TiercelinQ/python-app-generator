# Structure config.py et dépendances

## config.py — structure minimale obligatoire

```python
# config.py
APP_NAME: str = "NomApp"
APP_VERSION: str = "1.0.0"

# Base de données (si applicable)
DB_PATH: str = "data/nom_app.db"

# Préférences (si applicable)
PREFERENCES_FILE: str = "preferences.json"

# Internationalisation (si activée)
DEFAULT_LOCALE: str = "fr"
SUPPORTED_LOCALES: list[str] = ["fr", "en"]

# Couleurs primaires — remplacer ces 4 valeurs pour changer la couleur primaire
PRIMARY_50:  str = "#EEF2FF"   # fond sélection clair
PRIMARY_400: str = "#818CF8"   # texte actif sombre
PRIMARY_600: str = "#4F46E5"   # texte/bordure actif clair
PRIMARY_900: str = "#312E81"   # fond sélection sombre

# Icônes qtawesome — couleurs par thème (contrainte technique : non stylable via QSS)
ICON_COLORS: dict = {
    "light": {
        "default":  "#6B7280",   # text-subtle
        "active":   "#4F46E5",   # primary-600
        "danger":   "#DC2626",   # danger-600
        "success":  "#16A34A",   # success-600
        "muted":    "#9CA3AF",   # text-muted
    },
    "dark": {
        "default":  "#9CA3AF",   # text-subtle sombre
        "active":   "#818CF8",   # primary-400
        "danger":   "#F87171",   # danger-600 sombre
        "success":  "#4ADE80",   # success-600 sombre
        "muted":    "#6B7280",   # text-muted sombre
    }
}
```

Si couleur primaire personnalisée choisie en Phase 1 : remplacer `PRIMARY_*` et `ICON_COLORS[*]["active"]`.
Le `design-system.md` global reste inchangé.

Toute constante réutilisée dans plus d'un fichier va dans `config.py`.

## Préférences persistées — valeurs par défaut

| Préférence       | Valeur par défaut |
| ---------------- | ----------------- |
| thème            | système OS        |
| fenêtre taille   | 1280×800          |
| fenêtre position | centrée           |
| drawer état      | fermé             |

## requirements.txt — versioning loose

```
PyQt6>=6.7.0
qtawesome>=1.3.0
```

Versions loose (`>=`), fixées à la version minimale validée en Phase 1.

## Internationalisation (si activée)

- Toutes les chaînes visibles passent par `self.tr("texte")` dans les Views.
- Fichiers dans `resources/i18n/` : `app_fr.ts` et `app_en.ts`, compilés en `.qm`.
- Langue chargée au démarrage depuis préférences, FR par défaut.
- Changement de langue : redémarrage (pas de rechargement à chaud).
- Zéro chaîne en dur dans Views, Controllers ou Models.

## Packaging Windows (.exe) — sur demande explicite uniquement

```
pyinstaller --onefile --windowed --name NomApp main.py
            --add-data "resources;resources"
            --icon resources/icon.ico
```

Livré dans le dernier lot si demande explicite : `build.spec` commenté + instructions.
