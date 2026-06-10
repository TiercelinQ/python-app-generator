---
description: Phase 4 du cycle de développement — contrat architectural.
  Invoquer après validation de la Phase 3.
model: claude-sonnet-4-6
---

## Instructions — Phase 4 : Contrat architectural

Présenter l'arborescence complète du projet avec le rôle de chaque fichier, puis le tableau tokens QSS.

Format de sortie :

```
## Contrat architectural — [NOM_APP]

### Arborescence

[nom_app]/
├── main.py                        # Point d'entrée — instancie QApplication et MainWindow
├── config.py                      # Constantes globales, ICON_COLORS, PRIMARY_*
├── requirements.txt               # Dépendances PyQt6, qtawesome
├── preferences.json               # Généré au premier lancement (si préférences activées)
├── models/
│   ├── __init__.py
│   ├── exceptions.py              # Exceptions métier nommées
│   └── [entite]_model.py          # [description rôle]
├── views/
│   ├── __init__.py
│   ├── main_window.py             # Fenêtre principale, topbar, layout global
│   ├── toast_manager.py           # Système de toasts (position, animation, file)
│   └── [entite]_view.py           # [description rôle]
├── controllers/
│   ├── __init__.py
│   └── [entite]_controller.py     # [description rôle]
├── utils/
│   └── helpers.py                 # Fonctions pures (formatage, JSON, validation)
└── resources/
    ├── styles_light.qss           # Thème clair — tous tokens design-system.md
    └── styles_dark.qss            # Thème sombre — tous tokens design-system.md

### Tableau tokens → règles QSS

| Token design-system.md | Valeur clair | Valeur sombre | Règle QSS cible |
| ----------------------- | ------------ | ------------- | --------------- |
| bg                      | #FFFFFF      | #111827       | QMainWindow, #main_content, #topbar |
| bg-muted                | #F3F4F6      | #1F2937       | QStatusBar, hover, #toast_* |
| text                    | #111827      | #F9FAFB       | QMainWindow, QLabel |
| primary-600             | #4F46E5      | —             | QTabBar::tab:selected, #btn_primary |
| primary-400             | —            | #818CF8       | QTabBar::tab:selected (sombre) |
| border                  | #E5E7EB      | #374151       | QWidget#topbar, QStatusBar, QDialog |
| …                       | …            | …             | …               |
```

Terminer par :

```
→ Ce contrat est verrouillé après validation.
  Tout écart ultérieur (fusion, scission, renommage, ajout, suppression) impose :
  1. Arrêt.
  2. Déclaration de l'écart + justification.
  3. Validation avant reprise.

  Confirmer pour démarrer la Phase 5.
```

**Règle bloquante** : ne pas livrer le Lot 1 tant que la validation n'est pas explicite.
