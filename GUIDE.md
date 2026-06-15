# Guide d'utilisation — Python App Generator (unifié)

> Version unifiée : pipeline de génération + skills de maintenance, rôle explicite par skill, specs persistées, vérification exécutable, mémoire native.

---

## Structure du framework

```
claude-python-framework/
├── CLAUDE.md                 # Instructions core (EN) · persona · communication FR · index commandes · calibrage
├── design-system.md          # Référence visuelle contraignante (v1.1) — source de vérité unique
├── layout.md                 # Référence layout contraignante (v2.1) — 6 positions de toasts
├── rules/
│   ├── mvc.md                # Séparation MVC, livraison par lots, nettoyage anomalies
│   ├── qss.md                # Règles QSS, tokens light/dark, flat design
│   ├── errors.md             # Protocole erreurs, toasts, sys.excepthook
│   ├── config.md             # config.py, requirements, packaging, dérivation couleurs HSL
│   ├── security.md           # Validation entrées, SQL paramétré, secrets keyring, anti-injection
│   ├── tests.md              # pytest + pytest-qt, couverture par couche
│   ├── logging.md            # logging stdlib + RotatingFileHandler
│   ├── i18n.md               # Workflow .ts/.qm, pylupdate6 / lrelease
│   ├── db.md                 # Migrations versionnées SQLite/PostgreSQL/JSON/CSV
│   └── verification.md       # Vérification EXÉCUTABLE centralisée + intégrité statique
├── skills/
│   ├── python-app/           # Menu démarrage / reprise / maintenance (4 options)
│   ├── p1-scoping/       # Scoping — 6 questions + couleur → docs/specs/01-scoping.md
│   ├── p2-featuring/       # Fiche besoins + calibrage figé → docs/specs/02-featuring.md
│   ├── p3-designing/        # Proposition layout + personnalisation → docs/specs/03-designing.md
│   ├── p4-architect/       # Contrat architectural verrouillé → docs/specs/04-architect.md
│   ├── p5-development/ # Livraison par lots (enchaînement auto)
│   ├── add-feature/          # Ajouter une feature à un projet livré (diff de contrat)
│   ├── trace-feature/              # Tracer une fonctionnalité à travers les couches
│   ├── fix-issue/                  # Corriger un bug — arbre de décision, cause racine
│   ├── refactor-code/             # Restructurer sous validation explicite uniquement
│   ├── run-tests/                 # Vérification exécutable (ruff, mypy, pytest, smoke)
│   ├── load-project/       # Chargement d'un projet existant
│   ├── generate-readme/      # Génération README.md projet existant
│   ├── save-session/              # Sauvegarde de session
│   ├── show-state/               # État courant du projet
│   ├── show-contract/              # Arborescence du contrat validé
│   └── save-memory/            # Persiste dans la mémoire native Claude Code
├── settings.json             # Permissions d'exécution (python, pip, pytest, ruff, mypy)
├── GUIDE.md                  # Ce fichier
└── README.md                 # Présentation du repo GitHub (EN)
```

> Structure **plate** : un seul `design-system.md` et un seul `layout.md` (source de vérité unique — plus de duplicats racine/`.claude`). `CLAUDE.md` les importe via `@`.

---

## Nouveautés de la version unifiée

| Apport                        | Détail                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------- |
| **Rôle par skill**            | Chaque skill ouvre sur un persona ciblé (Role / Goal / Deliverable).            |
| **Specs persistées**          | Phases 1→4 écrivent `docs/specs/01-scoping.md` … `04-architect.md` (en français). |
| **Contrat = source de vérité**| `docs/specs/04-architect.md` relu par `/load-project`, `/show-contract`, `/add-feature`, `/refactor-code`. |
| **Skills de maintenance**     | `trace-feature`, `fix-issue`, `refactor-code`, `run-tests` (+ `add-feature`) avec arbres de décision et anti-patterns. |
| **Vérification exécutable**   | `rules/verification.md` : ruff, mypy, pytest, smoke — échec bloquant.           |
| **Mémoire native**            | `/save-memory` écrit dans la mémoire native Claude Code + `MEMORY.md`.            |

---

## Installation

```bash
# Copier le dossier du framework dans le projet cible (ou démarrer dedans)
# Claude Code détecte CLAUDE.md automatiquement.
claude
```

### Prérequis

```bash
claude --version      # Claude Code CLI installé et connecté
python --version      # Python 3.10+ (pour exécuter les apps générées)
```

### Activer la mémoire (une seule fois, par machine)

```
/config → Memory → Enable auto memory → On
```

Sans cette activation, `/save-memory` formule les notes mais ne les persiste pas entre sessions.

---

## Démarrer une nouvelle application

```
/python-app → 1
```

### Phase 1 — Scoping

6 questions en un seul bloc : objectif · base de données (SQLite / PostgreSQL / JSON / CSV / aucune) · préférences persistantes · i18n FR/EN · tests (pytest + pytest-qt) · packaging .exe (PyInstaller). Puis choix de couleur primaire : Steel Blue recommandé par défaut + 4 propositions adaptées au contexte ; l'utilisateur fournit `primary-600`, Claude dérive les autres via formule HSL.

Calibrage **provisoire** annoncé (figé après Phase 2) :

| Taille        | Lots (sans tests) | Lots (avec tests) |
| ------------- | ----------------- | ----------------- |
| Petit         | 3                 | 4                 |
| Moyen / Grand | 4                 | 5                 |

Écrit `docs/specs/01-scoping.md`.

### Phase 2 — Featuring

Fiche structurée + calibrage **confirmé** à partir du compte réel. Validation bloquante avant Phase 3. Écrit `docs/specs/02-featuring.md`.

### Phase 3 — Designing

Proposition issue de `layout.md` + personnalisation (onglets, drawer/modale, 6 positions de toasts). Validation bloquante. Écrit `docs/specs/03-designing.md`.

### Phase 4 — Architect

Arborescence + rôle de chaque fichier + tableau tokens → QSS + mapping source→test. **Verrouillé après validation.** Écrit `docs/specs/04-architect.md` (source de vérité).

### Phase 5 — Development

Claude crée les dossiers et écrit les fichiers directement sur le disque. Annonce `Lot N/[total] — [contenu]`. Enchaînement automatique. Découpage selon la table de `rules/mvc.md` (conditionnel tests). Dernier lot : instructions d'installation + `README.md` à la racine + `scripts/seed.py` (jeu de données cohérent si une base est présente). Vérification exécutable appliquée (`rules/verification.md`).

---

## Reprendre une session

```
/save-session            # sauvegarder en fin de session (docs/sessions/)
/python-app → 2     # reprendre : fournir le chemin du fichier SESSION
```

---

## Travailler sur un projet livré

```
/python-app → 3       # ou directement /load-project depuis la racine du projet
```

Claude lit `docs/specs/04-architect.md` (priorité), sinon le README, sinon le code, puis applique toutes les règles. Projet sans README : `/generate-readme`.

### Maintenance (`/python-app → 4`)

| Besoin                          | Commande      |
| ------------------------------- | ------------- |
| Ajouter une fonctionnalité      | `/add-feature` |
| Comprendre / tracer le code     | `/trace-feature`     |
| Corriger un bug                 | `/fix-issue`         |
| Restructurer (sous validation)  | `/refactor-code`    |
| Vérifier le build / lancer les checks | `/run-tests`  |

---

## Vérification exécutable

`rules/verification.md` est la source unique. Commandes (échec bloquant quand l'environnement le permet) :

```bash
python -m venv .venv ; .venv\Scripts\activate
pip install -r requirements.txt        # + requirements-dev.txt si tests/outillage
ruff check .                           # lint
ruff format --check .                  # format
mypy .                                 # type-check strict
pytest                                 # si tests activés uniquement
python main.py                         # smoke launch
```

`/run-tests` exécute cette échelle ; `/fix-issue` y renvoie pour confirmer une correction.

---

## Gestion des anomalies et mémoire

Après correction (`/fix-issue` ou Phase 5), Claude produit un bilan de nettoyage (éléments des tentatives infructueuses à retirer) puis propose `Veux-tu mémoriser ce point ? /save-memory`.

`/save-memory` catégorise (erreur / décision / préférence / autre) et écrit dans la **mémoire native Claude Code** (+ pointeur dans `MEMORY.md`), disponible dans les sessions suivantes.

---

## Commandes de référence

| Commande                | Modèle | Action                                               |
| ----------------------- | ------ | ---------------------------------------------------- |
| `/python-app`           | Haiku  | Menu démarrage / reprise / maintenance               |
| `/p1-scoping`       | Sonnet | Scoping — 6 questions + couleur (HSL)                |
| `/p2-featuring`       | Sonnet | Fiche besoins + calibrage figé                       |
| `/p3-designing`        | Sonnet | Proposition layout + personnalisation                |
| `/p4-architect`       | Sonnet | Contrat architectural verrouillé                     |
| `/p5-development` | Sonnet | Livraison par lots — enchaînement automatique        |
| `/add-feature`          | Sonnet | Ajouter une feature à un projet livré (diff)         |
| `/trace-feature`              | Sonnet | Tracer une fonctionnalité à travers les couches      |
| `/fix-issue`                  | Sonnet | Corriger un bug — cause racine                       |
| `/refactor-code`             | Sonnet | Restructurer sous validation                         |
| `/run-tests`                 | Sonnet | Vérification exécutable                               |
| `/load-project`       | Haiku  | Charger un projet existant                           |
| `/generate-readme`      | Sonnet | Générer README.md d'un projet existant               |
| `/save-session`              | Haiku  | Sauvegarder la session                               |
| `/show-state`               | Haiku  | État courant                                         |
| `/show-contract`              | Haiku  | Contrat architectural validé                         |
| `/save-memory`            | Haiku  | Persister dans la mémoire native                     |

---

## Structure d'une application générée

```
mon-app/
├── main.py                        # Point d'entrée — logger, migrations, excepthook
├── config.py                      # Constantes, PRIMARY_*, ICON_COLORS
├── requirements.txt · pyproject.toml
├── README.md                      # Généré en fin de Phase 5
├── CLAUDE.md                      # Identité projet (origine, contexte, écarts) — généré en fin de Phase 5
├── .claude/settings.json          # Garde-fous + hook de vérification (app auto-contrôlée)
├── docs/specs/                    # Specs de génération (FR)
├── models/                        # exceptions.py, db.py + migrations.py (si DB), [entite]_model.py
├── views/                         # main_window.py, toast_manager.py, [entite]_view.py
├── controllers/                   # [entite]_controller.py
├── utils/                         # helpers.py, logger.py
└── resources/                     # styles_light.qss, styles_dark.qss, i18n/ (si activé)

# Si tests activés en Phase 1 :
tests/                             # Miroir de la structure source
requirements-dev.txt
```

---

## Points de vigilance

- `design-system.md` (v1.1) et `layout.md` (v2.1) sont la **source de vérité unique** — ne pas les dupliquer ni modifier sans bump de version.
- Les couleurs d'icônes qtawesome sont dans `config.py` (`ICON_COLORS`), pas dans QSS (contrainte technique).
- Le contrat (`docs/specs/04-architect.md`) est verrouillé. Tout changement structurel passe par `/add-feature` ou le protocole de déclaration d'écart.
- `/load-project`, `/generate-readme`, `/add-feature`, `/trace-feature`, `/fix-issue`, `/refactor-code`, `/run-tests` s'invoquent depuis la racine du projet cible.
- `build.spec` est versionné (non gitignoré) si packaging Phase 1 Q6 = Oui.
- Toutes les commandes shell des skills sont compatibles Windows PowerShell.
