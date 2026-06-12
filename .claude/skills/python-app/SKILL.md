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
2. Reprendre une session (fichier SESSION)
3. Charger un projet existant (README.md à la racine)
4. Générer le README d'un projet existant (analyse code)

→ Réponds 1, 2, 3 ou 4.
```

Routage :

- `1` → enchaîner immédiatement sur le skill `/phase1-cadrage`.
- `2` → demander le chemin du fichier SESSION :
  ```
  Indique le chemin vers ton fichier SESSION :
  (ex: C:\projets\mon-app\claude-sessions\SESSION_MonApp_S1.md)
  ```
  Lire le fichier via l'outil natif `Read` (jamais `cat` — compatible Windows),
  puis invoquer le skill `/session` pour la reprise.
- `3` → invoquer le skill `/charger-projet`.
- `4` → invoquer le skill `/generate-readme`.

Si tapé en cours de projet : afficher le menu uniquement, sans réinitialiser le contexte.
