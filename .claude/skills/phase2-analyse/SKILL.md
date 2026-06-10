---
description: Phase 2 du cycle de développement — analyse des besoins.
  Invoquer après la Phase 1 pour structurer les besoins avant le layout.
model: claude-sonnet-4-6
---

## Instructions — Phase 2 : Analyse des besoins

Produire une fiche structurée :

```
## Analyse des besoins — [NOM_APP]

**Objectif**
[Description synthétique de l'application]

**Fonctionnalités retenues**
- [Fonctionnalité 1]
- [Fonctionnalité 2]
- …

**Hors périmètre**
- [Ce qui est explicitement exclu]

**Contraintes techniques**
- OS : Windows · PyQt6 · Python 3.10+
- DB : [valeur choisie en Phase 1]
- Préférences : [Oui/Non]
- i18n : [Oui/Non]
- Couleur primaire : [choix Phase 1]
```

Terminer par :

```
→ Validation requise avant Phase 3.
  Confirmer ou lister les ajustements.
```

**Règle bloquante** : ne pas passer à Phase 3 tant que la validation n'est pas explicite.
Si validation partielle : lister les points ouverts, bloquer jusqu'à résolution complète.
