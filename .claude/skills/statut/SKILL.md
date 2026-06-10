---
description: Affiche l'état courant du projet en cours (phase, lot, décisions verrouillées, points ouverts).
disable-model-invocation: true
model: claude-haiku-4-5
---

Afficher exactement ce format :

```
Phase : [nom] | Lot : [X/total] | Prochain : [action attendue]
Décisions verrouillées : [liste]
Points ouverts : [liste ou "aucun"]
```

Si aucun projet en cours : "Aucun projet actif. Taper /python-app pour démarrer."

Ne pas ajouter `/session · /statut · /contrat` en fin de réponse.
