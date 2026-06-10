---
description: Phase 1 du cycle de développement — cadrage d'une nouvelle application.
             Invoquer immédiatement quand l'utilisateur choisit "1. Nouvelle application".
model: claude-sonnet-4-6
---

## Instructions — Phase 1 : Cadrage

Poser les 4 questions suivantes en **un seul bloc** :

```
1. Objectif de l'application — description libre.
2. Base de données : SQLite / PostgreSQL / JSON / CSV / aucune ?
3. Préférences persistantes entre sessions (thème, fenêtre…) ? Oui / Non
4. Internationalisation FR/EN activée pour ce projet ? Oui / Non (FR par défaut si Non)
```

Après réception des réponses, proposer le choix de couleur primaire :

```
Couleur primaire pour ce projet :

A. [Couleur 1] — [hex clair] / [hex sombre] — [caractère en 3 mots]
B. [Couleur 2] — [hex clair] / [hex sombre] — [caractère en 3 mots]
C. [Couleur 3] — [hex clair] / [hex sombre] — [caractère en 3 mots]
D. Slate Blue  — #4F46E5 / #818CF8          — professionnel, tech, sobre (défaut)
```

Règles couleur :
- Proposer 3 couleurs professionnelles adaptées au contexte de l'application décrite.
- Si A/B/C : `PRIMARY_50`, `PRIMARY_400`, `PRIMARY_600`, `PRIMARY_900` définis dans `config.py` et `styles.qss`. Le `design-system.md` global reste inchangé.
- Si D ou pas de réponse : Slate Blue par défaut.

Après le choix de couleur, annoncer le calibrage :

```
Calibrage : [Petit | Moyen/Grand] — [N] lots
(Ce nombre est figé. Aucune modification possible après validation.)
```

| Taille        | Fichiers | Fonctionnalités | Lots |
| ------------- | -------- | --------------- | ---- |
| Petit         | < 10     | ≤ 5             | 3    |
| Moyen / Grand | ≥ 10     | > 5             | 4    |

Enchaîner immédiatement sur la Phase 2 (skill `/phase2-analyse`).