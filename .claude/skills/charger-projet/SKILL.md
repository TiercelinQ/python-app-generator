---
description: Charge le contexte d'un projet finalisé depuis son README.md.
             Invoquer en début de session sur un projet existant avant toute
             intervention (développement, correction, amélioration, ajustement).
model: claude-haiku-4-5
disable-model-invocation: true
---

## Analyse du projet

Utiliser les outils natifs Claude Code (compatible Windows) :

1. **Lire** `README.md` à la racine via l'outil `Read`.
2. **Détecter `tests/`** via l'outil `Glob` avec le pattern `tests/**/*.py`
   → compter les fichiers retournés pour `[N]`.

## Instructions

Confirmer la prise en charge avec ce format exact :

```
Projet [NOM_APP] v[VERSION] chargé.

Stack    : [résumé une ligne issu du README]
DB       : [valeur]
Fonctionnalités : [N] — [liste courte]
Architecture    : [N] fichiers — MVC PyQt6
Tests    : [présents ([N] fichiers) | absents]

Prêt pour : développement · corrections · améliorations · ajustements.
```

Appliquer immédiatement toutes les règles du `CLAUDE.md` pour toute intervention
sur ce projet : MVC strict, QSS uniquement, toasts, design-system.md, layout.md,
tests.md si tests présents.
