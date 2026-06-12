---
description: Génère le fichier de sauvegarde de session pour reprendre le projet plus tard.
model: claude-haiku-4-5
disable-model-invocation: true
---

## Sauvegarde de session

Utiliser les outils natifs Claude Code (compatible Windows) :

1. **Créer** le dossier `claude-sessions/` s'il n'existe pas, via l'outil `Shell` :
   `mkdir claude-sessions` (PowerShell — silencieux si déjà présent grâce à `-Force` :
   `New-Item -ItemType Directory -Force -Path claude-sessions | Out-Null`).
2. **Écrire** le fichier `claude-sessions/SESSION_[nom_app]_S[N].md` via l'outil `Write`
   (jamais via `cat`/heredoc — incompatible Windows).

Numérotation `[N]` :
1. Lister les fichiers existants via `Glob` avec le pattern `claude-sessions/SESSION_*_S*.md`.
2. Extraire les entiers `N` de chaque nom (regex `S(\d+)\.md$`).
3. `[N]` = `max(entiers) + 1`, ou `1` si aucun fichier.
4. `[nom_app]` = valeur exacte de `APP_NAME` dans `config.py` (sans espaces).

## Contenu du fichier SESSION

```
# SESSION_S[N] — [NOM_APP] · [Phase terminée]

## Statut

Phase terminée : [N — nom]
Phase suivante : [N+1 — nom]
Lot suivant : [X+1/total] (si Phase 5)

## Décisions verrouillées

- OS : Windows · Framework : PyQt6
- DB : [valeur]
- Préférences : [Oui/Non]
- i18n : [Oui/Non]
- Tests : [Oui/Non] — pytest + pytest-qt si Oui
- Couleur primaire : [choix + hex]
- Fonctionnalités retenues : [liste]
- Hors périmètre : [liste]
- Layout retenu : [description]
- Calibrage : [N] lots (dont 1 lot tests si activé)

## Contrat architectural

[Arborescence complète — copiée de Phase 4, incluant tests/ si activé]

## Lots livrés

- [x] Lot 1 — [contenu]
- [ ] Lot 2 — [contenu]
- ...

## Points ouverts

[liste ou "aucun"]
```

## Confirmation

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 SAUVEGARDE SESSION
Fichier écrit : claude-sessions/SESSION_[nom_app]_S[N].md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Ne pas ajouter `/session · /statut · /contrat` en fin de réponse.

## Reprise depuis un fichier SESSION

Si le message contient un bloc SESSION (ou si l'utilisateur fournit un chemin) :

1. **Lire** le fichier via l'outil `Read`.
2. Répondre : `📋 Reprise [NOM_APP] — [Phase suivante] | Lot [X/total] | Points ouverts : [liste ou "aucun"]`
3. Enchaîner immédiatement sans re-poser les questions déjà résolues.
4. Invoquer le skill correspondant à la phase suivante.
