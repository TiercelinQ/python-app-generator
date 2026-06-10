---
description: Menu de démarrage du générateur d'applications Python/PyQt6.
             Invoquer pour démarrer ou reprendre un projet.
model: claude-haiku-4-5
disable-model-invocation: true
---

Afficher exactement ce menu :

```
Que faire ?

1. Nouvelle application
2. Reprendre une application existante

→ Réponds 1 ou 2.
```

- Si l'utilisateur répond `1` : enchaîner immédiatement sur le skill `/phase1-cadrage`.
- Si l'utilisateur répond `2` : demander le chemin du fichier SESSION :
  ```
  Indique le chemin vers ton fichier SESSION :
  (ex: C:\projets\mon-app\claude-sessions\SESSION_MonApp_S1.md)
  ```
  Lire le fichier via `!`cat [chemin fourni]`` puis invoquer le skill `/session`.
- Si tapé en cours de projet : afficher le menu uniquement, sans réinitialiser.