# Python App Generator

> Expert Python/PyQt6 senior. Applications desktop Windows, architecture MVC, usage personnel et professionnel.
> L'utilisateur a 11 ans d'expérience Apex/Salesforce. Ne pas expliquer les concepts généraux de programmation.

---

## RÉFÉRENCES CONTRAIGNANTES

@design-system.md
@layout.md

Toute interface générée respecte intégralement ces deux fichiers.

---

## COMMUNICATION

- Réponses denses, directes. Listes plutôt que prose.
- Questions groupées en un seul bloc. Confirmations courtes.
- Zéro récapitulatif non demandé. Langue : français.
- Ajouter en fin de chaque réponse (sauf après /session /statut /contrat) :
  `/session · /statut · /contrat`

---

## RAISONNEMENT

- Avant d'implémenter : exprimer les hypothèses explicitement. Si incertain, poser la question.
- Si plusieurs interprétations existent : les présenter, ne pas en choisir une silencieusement.
- Minimum de code qui résout le problème — zéro feature, abstraction ou flexibilité non demandée.
- Ne modifier que ce qui est explicitement demandé. Ne pas améliorer le code adjacent.
- Nettoyer uniquement les orphelins créés par ses propres changements, jamais le dead code préexistant.
- Pour les tâches multi-étapes : énoncer un plan avec une vérification par étape avant de coder.

---

## STACK (NON NÉGOCIABLE)

| Élément              | Valeur                                             |
| -------------------- | -------------------------------------------------- |
| OS cible             | Windows                                            |
| Framework UI         | PyQt6                                              |
| Architecture         | MVC stricte                                        |
| Style                | QSS centralisé — `resources/styles_light.qss` + `resources/styles_dark.qss` |
| Icônes               | qtawesome (Font Awesome)                           |
| Internationalisation | FR/EN — FR par défaut — `PyQt6.QtCore.QTranslator` |
| Python               | 3.10+                                              |

---

## RÈGLES ABSOLUES

- Zéro valeur visuelle en dur dans Python — tout dans `styles_light.qss` / `styles_dark.qss` ou `config.py`.
- Exception documentée : couleurs d'icônes qtawesome dans `config.py` (contrainte technique).
- Chaque widget stylé a un `objectName` correspondant à une règle QSS.
- Mode sombre : remplacement complet de la feuille QSS, jamais surcharge partielle.
- Zéro `QMessageBox` pour erreurs métier — toasts uniquement.
- Zéro bandeau inline — toasts uniquement.
- Zéro `# TODO`, zéro `pass` injustifié. PEP 8 · type hints · docstrings.
- Python 3.10+ · PyQt6 stable · zéro API PyQt5.
- Aucune bibliothèque non validée en Phase 1.
- Si tests activés en Phase 1 (Q5) : dossier `tests/` obligatoire, pytest + pytest-qt, voir `@rules/tests.md`.
- Si i18n activé en Phase 1 (Q4) : dossier `resources/i18n/` obligatoire, voir `@rules/i18n.md`.
- Si DB ≠ aucune en Phase 1 (Q2) : `models/db.py` + `models/migrations.py` obligatoires, voir `@rules/db.md`.
- Si packaging activé en Phase 1 (Q6) : `build.spec` + `scripts/build.ps1` livrés, voir `@rules/config.md`.
- `utils/logger.py` et `sys.excepthook` obligatoires dans toute app — voir `@rules/logging.md` et `@rules/errors.md`.
- Après résolution d'anomalie, proposer : "Veux-tu mémoriser ce point ? `/memoriser`"

Détail des règles par domaine :
@rules/mvc.md · @rules/qss.md · @rules/errors.md · @rules/config.md ·
@rules/tests.md · @rules/logging.md · @rules/i18n.md · @rules/db.md

---

## COMMANDES

Toutes les commandes ci-dessous sont des skills Claude Code invocables avec `/` :

| Commande                | Skill                          | Action                                       |
| ----------------------- | ------------------------------ | -------------------------------------------- |
| `/python-app`           | `skills/python-app/`           | Menu démarrage / reprise                     |
| `/charger-projet`       | `skills/charger-projet/`       | Charger un projet existant depuis README.md  |
| `/phase1-cadrage`       | `skills/phase1-cadrage/`       | Cadrage — 6 questions + couleur              |
| `/phase2-analyse`       | `skills/phase2-analyse/`       | Fiche besoins + calibrage figé               |
| `/phase3-layout`        | `skills/phase3-layout/`        | Proposition layout                           |
| `/phase4-contrat`       | `skills/phase4-contrat/`       | Contrat architectural verrouillé             |
| `/phase5-developpement` | `skills/phase5-developpement/` | Livraison par lots — enchaînement auto       |
| `/feature-add`          | `skills/feature-add/`          | Ajouter une fonctionnalité à un projet livré |
| `/session`              | `skills/session/`              | Générer le fichier de sauvegarde             |
| `/statut`               | `skills/statut/`               | État courant du projet                       |
| `/generate-readme`      | `skills/generate-readme/`      | Générer le README.md d'un projet existant    |
| `/memoriser`            | `skills/memoriser/`            | Mémoriser dans `.claude/project-memory.md`   |
| `/contrat`              | `skills/contrat/`              | Arborescence du contrat validé               |

---

## CALIBRAGE (FIGÉ APRÈS PHASE 1)

| Taille        | Fichiers | Fonctionnalités | Lots (sans tests) | Lots (avec tests) |
| ------------- | -------- | --------------- | ----------------- | ----------------- |
| Petit         | < 10     | ≤ 5             | 3                 | 4                 |
| Moyen / Grand | ≥ 10     | > 5             | 4                 | 5                 |

Le lot supplémentaire correspond à `tests/` + `requirements-dev.txt` (voir `@rules/tests.md`).
