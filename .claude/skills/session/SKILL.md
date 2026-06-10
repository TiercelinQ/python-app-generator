---
description: Génère le fichier de sauvegarde de session pour reprendre le projet plus tard.
disable-model-invocation: true
---

Exécuter les commandes suivantes avant de générer le bloc :

```bash
mkdir -p claude-sessions
```

Puis écrire le fichier SESSION directement :

```bash
cat > claude-sessions/SESSION_[nom_app]_S[N].md << 'EOF'
[contenu du fichier SESSION]
EOF
```

Confirmer avec :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 SAUVEGARDE SESSION
Fichier écrit : claude-sessions/SESSION_[nom_app]_S[N].md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# SESSION_S[N] — [NOM_APP] · [Phase terminée]

## Statut

Phase terminée : [N — nom]
Phase suivante : [N+1 — nom]
Lot suivant : [X+1/total] (si Phase 5)

## Décisions verrouillées

- OS : Windows · Framework : PyQt6
- DB : [valeur]
- Couleur primaire : [choix + hex]
- Fonctionnalités retenues : [liste]
- Hors périmètre : [liste]
- Layout retenu : [description]
- Calibrage : [N] lots

## Contrat architectural

[Arborescence complète — copiée de Phase 4]

## Lots livrés

- [x] Lot 1 — [contenu]
- [ ] Lot 2 — [contenu]

## Points ouverts

[liste ou "aucun"]
```

Ne pas ajouter `/session · /statut · /contrat` en fin de réponse.

## Reprise depuis un fichier SESSION

Si le message contient un bloc SESSION :

1. Lire le bloc intégralement.
2. Répondre : `📋 Reprise [NOM_APP] — [Phase suivante] | Lot [X/total] | Points ouverts : [liste ou "aucun"]`
3. Enchaîner immédiatement sans re-poser les questions déjà résolues.
4. Invoquer le skill correspondant à la phase suivante.