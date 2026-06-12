---
description: Phase 1 du cycle de développement — cadrage d'une nouvelle application.
             Invoquer immédiatement quand l'utilisateur choisit "1. Nouvelle application".
model: claude-sonnet-4-6
---

## Instructions — Phase 1 : Cadrage

Poser les 6 questions suivantes en **un seul bloc** :

```
1. Objectif de l'application — description libre.
2. Base de données : SQLite / PostgreSQL / JSON / CSV / aucune ?
3. Préférences persistantes entre sessions (thème, fenêtre…) ? Oui / Non
4. Internationalisation FR/EN activée pour ce projet ? Oui / Non (FR par défaut si Non)
5. Tests automatisés (pytest + pytest-qt) ? Oui / Non — recommandé Oui pour usage pro
6. Packaging .exe (PyInstaller — build.spec + script PowerShell) ? Oui / Non
```

Après réception des réponses, proposer le choix de couleur primaire :

```
Couleur primaire pour ce projet (un seul hex `primary-600` suffit — Claude dérive les 3 autres) :

A. [Couleur 1] — primary-600 = [hex] — [caractère en 3 mots]
B. [Couleur 2] — primary-600 = [hex] — [caractère en 3 mots]
C. [Couleur 3] — primary-600 = [hex] — [caractère en 3 mots]
D. Slate Blue  — primary-600 = #4F46E5 — professionnel, tech, sobre (défaut)
E. Personnalisé — fournir un hex `primary-600` (ex: #2563EB)
```

Règles couleur (voir `@rules/config.md` section "Dérivation des tokens primaires") :

- Proposer 3 couleurs professionnelles adaptées au contexte de l'application décrite.
- À partir de la valeur `primary-600` retenue, Claude **dérive** automatiquement :
  - `primary-50`   = même teinte, luminosité ~95% (fond sélection clair)
  - `primary-400`  = même teinte, luminosité ~70% (texte actif sombre)
  - `primary-900`  = même teinte, luminosité ~25% (fond sélection sombre)
- Les 4 valeurs sont écrites dans `config.py` (`PRIMARY_*`) et `styles_light.qss` / `styles_dark.qss`.
- Le `design-system.md` global reste inchangé.
- Si D ou pas de réponse : Slate Blue par défaut (4 valeurs déjà connues).

Annoncer ensuite le calibrage **provisoire** :

```
Calibrage provisoire : [Petit | Moyen/Grand] — [N] lots (dont 1 lot tests si activé)
(Sera confirmé à la fin de la Phase 2, après comptage des fonctionnalités réelles.)
```

| Taille        | Fichiers | Fonctionnalités | Lots (sans tests) | Lots (avec tests) |
| ------------- | -------- | --------------- | ----------------- | ----------------- |
| Petit         | < 10     | ≤ 5             | 3                 | 4                 |
| Moyen / Grand | ≥ 10     | > 5             | 4                 | 5                 |

Enchaîner immédiatement sur la Phase 2 (skill `/phase2-analyse`).