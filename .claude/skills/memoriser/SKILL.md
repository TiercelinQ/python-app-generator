---
description: Mémorise un point important pour éviter de reproduire une erreur
             ou consolider une décision. Invoquer après résolution d'anomalie
             ou validation d'un choix structurant.
model: claude-haiku-4-5
disable-model-invocation: true
---

## Étape 1 — Catégoriser

Demander à l'utilisateur ce qu'il souhaite mémoriser :

```
Que veux-tu retenir ?

A. Une erreur à ne plus reproduire — décrire l'erreur et la solution retenue
B. Une décision structurante — décrire le choix et la raison
C. Une préférence de génération — décrire le comportement souhaité
D. Autre — décrire librement
```

## Étape 2 — Persister dans `.claude/project-memory.md`

Le fichier `.claude/project-memory.md` est versionné avec le projet (commitable).
Il complète la mémoire personnelle Claude Code (`~/.claude/agent-memory/`, locale machine).

Procédure (compatible Windows) :

1. Vérifier l'existence du fichier via `Glob` sur `.claude/project-memory.md`.
2. Si absent : créer via `Write` avec l'en-tête initial :
   ```markdown
   # Mémoire projet

   > Notes accumulées sur les erreurs à éviter, décisions structurantes et préférences.
   > Versionné avec le projet — partageable entre utilisateurs.
   ```
3. Lire le contenu existant via `Read`.
4. Construire le nouveau contenu = ancien + nouvelle note.
5. Écrire le tout via `Write`.

Format de la note ajoutée :

```markdown
---

## [YYYY-MM-DD] — [Catégorie : Erreur | Décision | Préférence | Note]

**Contexte** : [brève description de la situation]
**À retenir** : [formulation actionnable — ce que Claude doit faire ou éviter]
```

## Étape 3 — Confirmation

```
Mémorisé dans .claude/project-memory.md. Ce point sera appliqué dans les sessions
suivantes sur ce projet (et partagé si le fichier est commité).
```

Ne pas ajouter `/session · /statut · /contrat` en fin de réponse.
