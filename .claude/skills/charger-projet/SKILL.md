---
description: Charge le contexte d'un projet finalisé depuis son README.md.
             Invoquer en début de session sur un projet existant avant toute
             intervention (développement, correction, amélioration, ajustement).
model: claude-haiku-4-5
---

## README du projet

!`cat README.md`

## Instructions

Lire le README ci-dessus et confirmer la prise en charge avec ce format exact :

```
Projet [NOM_APP] v[VERSION] chargé.

Stack    : [résumé une ligne]
DB       : [valeur]
Fonctionnalités : [N] — [liste courte]
Architecture    : [N] fichiers — MVC PyQt6

Prêt pour : développement · corrections · améliorations · ajustements.
```

Appliquer immédiatement toutes les règles du CLAUDE.md pour toute intervention
sur ce projet : MVC strict, QSS uniquement, toasts, design-system.md, layout.md.