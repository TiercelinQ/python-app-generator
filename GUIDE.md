# Guide d'utilisation — Python App Generator (unifié)

> Version unifiée : pipeline de génération + skills de maintenance, rôle explicite par skill, specs persistées, vérification exécutable, mémoire native.

---

## Structure du framework

```
python-app-generator/
├── CLAUDE.md                 # Instructions core (EN) · persona · communication FR · index commandes · calibrage
├── GUIDE.md                  # Ce fichier
├── README.md                 # Présentation du repo GitHub (EN)
├── LICENSE
└── .claude/
    ├── design-system.md      # Référence visuelle contraignante (v2.0) — source de vérité unique
    ├── layout.md             # Cadre layout d'accompagnement (v4.1) — catalogue de patterns + composition par défaut + 6 positions de toasts
    ├── sf-cli-reference/     # Catalogue commandes/flags sf v2 (chargé par section si intégration Salesforce)
    ├── rules/
    │   ├── mvc.md            # Séparation MVC, livraison par lots, nettoyage anomalies
    │   ├── qss.md            # Règles QSS, tokens light/dark, profondeur par le trait
    │   ├── errors.md         # Protocole erreurs, toasts, sys.excepthook
    │   ├── config.md         # config.py, requirements, packaging, dérivation couleurs HSL
    │   ├── security.md       # Validation entrées, SQL paramétré, secrets keyring, anti-injection
    │   ├── tests.md          # pytest + pytest-qt, couverture par couche
    │   ├── logging.md        # logging stdlib + RotatingFileHandler
    │   ├── i18n.md           # Workflow .ts/.qm, pyside6-lupdate / pyside6-lrelease
    │   ├── db.md             # Migrations versionnées SQLite/PostgreSQL/JSON/CSV
    │   ├── sf-cli.md         # Intégration Salesforce CLI opt-in (runner subprocess, Org Manager)
    │   ├── splash.md         # Splash screen opt-in (QSplashScreen, icône, thème)
    │   ├── verification.md   # Vérification EXÉCUTABLE centralisée + intégrité statique
    │   └── readme.md         # Synchro README post-livraison (régénération auto)
    ├── skills/
    │   ├── python-app/              # Menu démarrage / reprise / maintenance (4 options)
    │   ├── python-p1-scoping/       # Scoping — 8 questions + couleur → docs/specs/01-scoping.md
    │   ├── python-p2-featuring/     # Fiche besoins + calibrage figé → docs/specs/02-featuring.md
    │   ├── python-p3-surfaces/     # Proposition layout + personnalisation → docs/specs/03-surfaces.md
    │   ├── python-p4-architect/     # Contrat architectural verrouillé → docs/specs/04-architect.md
    │   ├── python-p5-development/   # Livraison par lots (enchaînement auto)
    │   ├── python-add-feature/      # Ajouter une feature à un projet livré (diff de contrat)
    │   ├── python-trace-feature/    # Tracer une fonctionnalité à travers les couches
    │   ├── python-fix-issue/        # Corriger un bug — arbre de décision, cause racine
    │   ├── python-refactor-code/    # Restructurer sous validation explicite uniquement
    │   ├── python-migrate-design/   # Convertir une app v1.x vers le design system v2.0
    │   ├── python-release/          # Figer une version SemVer depuis le changelog cumulé
    │   ├── python-run-tests/        # Vérification exécutable (ruff, mypy, pytest, smoke)
    │   ├── python-load-project/     # Chargement d'un projet existant
    │   ├── python-generate-readme/  # Génération README.md projet existant
    │   ├── python-save-session/     # Sauvegarde de session
    │   ├── python-show-state/       # État courant du projet
    │   ├── python-show-contract/    # Arborescence du contrat validé
    │   └── python-save-memory/      # Persiste dans la mémoire native Claude Code
    ├── settings.json         # Permissions d'exécution (python, pip, pytest, ruff, mypy) + garde-fous deny (.env, secrets, build/dist)
    └── settings.local.json   # Overrides locaux (non versionné)
```

> Source de vérité **unique** : un seul `design-system.md` et un seul `layout.md`, sous `.claude/` (plus de duplicats racine/`.claude`, lus à la demande par les skills UI, non auto-importés — voir `CLAUDE.md` § BINDING REFERENCES). `design-system.md` est contraignant (skin) ; la composition décrite par `layout.md` est un **défaut modifiable**, co-défini en Phase 3 et verrouillé dans `docs/specs/04-architect.md`.

---

## Nouveautés de la version unifiée

| Apport                        | Détail                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------- |
| **Rôle par skill**            | Chaque skill ouvre sur un persona ciblé (Role / Goal / Deliverable).            |
| **Specs persistées**          | Phases 1→4 écrivent `docs/specs/01-scoping.md` … `04-architect.md` (dans la langue de l'utilisateur). |
| **Contrat = source de vérité**| `docs/specs/04-architect.md` relu par `/python-load-project`, `/python-show-contract`, `/python-add-feature`, `/python-refactor-code`. |
| **Skills de maintenance**     | `python-trace-feature`, `python-fix-issue`, `python-refactor-code`, `python-migrate-design`, `python-release`, `python-run-tests` (+ `python-add-feature`) avec arbres de décision et anti-patterns. |
| **Vérification exécutable**   | `rules/verification.md` : ruff, mypy, pytest, smoke — échec bloquant.           |
| **Mémoire native**            | `/python-save-memory` écrit dans la mémoire native Claude Code + `MEMORY.md`.            |

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
python --version      # Python 3.12+ (pour exécuter les apps générées)
```

### Activer la mémoire (une seule fois, par machine)

```
/config → Memory → Enable auto memory → On
```

Sans cette activation, `/python-save-memory` formule les notes mais ne les persiste pas entre sessions.

---

## Démarrer une nouvelle application

```
/python-app → 1
```

### Phase 1 — Scoping

8 questions en un seul bloc : objectif · base de données (SQLite / PostgreSQL / JSON / CSV / aucune) · préférences persistantes · i18n FR/EN · tests (pytest + pytest-qt) · icône `.ico` · packaging .exe (PyInstaller) · intégration Salesforce CLI (opt-in `sf` v2 ; défaut recommandé à Yes si l'objectif mentionne Salesforce). Puis choix de la **palette** : un accent obligatoire + jusqu'à 4 rôles optionnels (fond principal, fond secondaire, texte, détails) en override. Tout le reste est dérivé de l'accent : neutres teintés (les deux thèmes), stops d'accent, couleurs sémantiques harmonisées vers l'accent (info = accent). Palette « Steel Blue » par défaut + 5 palettes nommées (Teal, Forest, Slate, Amber, Ruby) + palette personnalisée ; contrôle de contraste WCAG AA (averti, non bloquant), y compris sur les paires sémantiques dérivées.

Calibrage **provisoire** annoncé (figé après Phase 2) :

| Taille        | Lots (sans tests) | Lots (avec tests) |
| ------------- | ----------------- | ----------------- |
| Petit         | 3                 | 4                 |
| Moyen / Grand | 4                 | 5                 |

Écrit `docs/specs/01-scoping.md`.

### Phase 2 — Featuring

Fiche structurée + calibrage **confirmé** à partir du compte réel. Validation bloquante avant Phase 3. Écrit `docs/specs/02-featuring.md`.

### Phase 3 — Surfaces

Co-conception guidée. Questionnaire structurant (navigation horizontale ou verticale, organisation du contenu, formulaires et actions) appuyé sur le catalogue de patterns de `layout.md` §12 : topbar + onglets (défaut), sidebar verticale, barre de menus (`QMenuBar`), master-detail (`QSplitter`). Puis proposition sur mesure, composition librement amendable, et questions de détail (position des onglets, drawer/modale, 6 positions de toasts, splash screen). Validation bloquante. Écrit `docs/specs/03-surfaces.md`.

> **Splash screen (opt-in)** : question Oui/Non (Oui recommandé). Si Oui, `QSplashScreen` affiché au démarrage jusqu'à ce que la fenêtre principale soit prête, suivant le design system (skin par le trait, palette, dark mode). Il affiche l'icône de l'app si définie (Phase 1) ; sinon, un chemin d'icône optionnel est demandé en Phase 3, à défaut le splash montre le nom de l'app. Couleurs du splash dans `config.py` (`SPLASH_COLORS`), 2e exception QSS documentée comme `ICON_COLORS`. Durée minimale configurable (`SPLASH_MIN_DURATION_MS`). Détail : `rules/splash.md`.

### Phase 4 — Architect

Arborescence + rôle de chaque fichier + tableau tokens → QSS + mapping source→test. **Verrouillé après validation.** Écrit `docs/specs/04-architect.md` (source de vérité).

### Phase 5 — Development

Claude crée les dossiers et écrit les fichiers directement sur le disque. Annonce `Lot N/[total] — [contenu]`. Enchaînement automatique. Découpage selon la table de `rules/mvc.md` (conditionnel tests). Dernier lot : instructions d'installation + `README.md` à la racine + `scripts/seed.py` (jeu de données cohérent si une base est présente). Vérification exécutable appliquée (`rules/verification.md`).

---

## Reprendre une session

```
/python-save-session            # sauvegarder en fin de session (docs/sessions/)
/python-app → 2     # reprendre : fournir le chemin du fichier SESSION
```

---

## Travailler sur un projet livré

```
/python-app → 3       # ou directement /python-load-project depuis la racine du projet
```

Claude lit `docs/specs/04-architect.md` (priorité), sinon le README, sinon le code, puis applique toutes les règles. Projet sans README : `/python-generate-readme`.

### Maintenance (`/python-app → 4`)

| Besoin                          | Commande      |
| ------------------------------- | ------------- |
| Ajouter une fonctionnalité      | `/python-add-feature` |
| Comprendre / tracer le code     | `/python-trace-feature`     |
| Corriger un bug                 | `/python-fix-issue`         |
| Restructurer (sous validation)  | `/python-refactor-code`    |
| Convertir une app v1.x vers le design system v2.0 | `/python-migrate-design` |
| Figer une version SemVer (changelog cumulé) | `/python-release` |
| Vérifier le build / lancer les checks | `/python-run-tests`  |

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

`/python-run-tests` exécute cette échelle ; `/python-fix-issue` y renvoie pour confirmer une correction.

---

## Gestion des anomalies et mémoire

Après correction (`/python-fix-issue` ou Phase 5), Claude produit un bilan de nettoyage (éléments des tentatives infructueuses à retirer) puis propose `Veux-tu mémoriser ce point ? /python-save-memory`.

`/python-save-memory` catégorise (erreur / décision / préférence / autre) et écrit dans la **mémoire native Claude Code** (+ pointeur dans `MEMORY.md`), disponible dans les sessions suivantes.

---

## Commandes de référence

| Commande                | Modèle | Action                                               |
| ----------------------- | ------ | ---------------------------------------------------- |
| `/python-app`           | Haiku  | Menu démarrage / reprise / maintenance               |
| `/python-p1-scoping`       | Sonnet | Scoping — 8 questions + couleur (HSL)                |
| `/python-p2-featuring`       | Sonnet | Fiche besoins + calibrage figé                       |
| `/python-p3-surfaces`        | Sonnet | Proposition layout + personnalisation                |
| `/python-p4-architect`       | Sonnet | Contrat architectural verrouillé                     |
| `/python-p5-development` | Sonnet | Livraison par lots — enchaînement automatique        |
| `/python-add-feature`          | Sonnet | Ajouter une feature à un projet livré (diff)         |
| `/python-trace-feature`              | Sonnet | Tracer une fonctionnalité à travers les couches      |
| `/python-fix-issue`                  | Sonnet | Corriger un bug — cause racine                       |
| `/python-refactor-code`             | Sonnet | Restructurer sous validation                         |
| `/python-migrate-design`            | Sonnet | Convertir une app v1.x vers le design system v2.0    |
| `/python-release`                   | Sonnet | Figer une version SemVer depuis le changelog cumulé  |
| `/python-run-tests`                 | Sonnet | Vérification exécutable                               |
| `/python-load-project`       | Sonnet | Charger un projet existant                           |
| `/python-generate-readme`      | Sonnet | Générer README.md d'un projet existant               |
| `/python-save-session`              | Haiku  | Sauvegarder la session                               |
| `/python-show-state`               | Haiku  | État courant                                         |
| `/python-show-contract`              | Haiku  | Contrat architectural validé                         |
| `/python-save-memory`            | Haiku  | Persister dans la mémoire native                     |

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
├── docs/specs/                    # Specs de génération (langue utilisateur)
├── docs/release/CHANGELOG.md      # Changelog SemVer (Keep a Changelog, anglais)
├── models/                        # exceptions.py, db.py + migrations.py (si DB), [entite]_model.py
├── views/                         # main_window.py, toast_manager.py, [entite]_view.py
├── controllers/                   # [entite]_controller.py
├── utils/                         # helpers.py, logger.py
└── resources/                     # styles_light.qss, styles_dark.qss, i18n/ (si activé)

# Si tests activés en Phase 1 :
tests/                             # Miroir de la structure source
requirements-dev.txt
```

### Versioning & changelog

Chaque app générée porte une version SemVer et un changelog `docs/release/CHANGELOG.md` (format Keep a Changelog, rédigé en anglais). Les skills de maintenance (`add-feature`, `fix-issue`, `refactor-code`, `migrate-design`) accumulent leurs entrées sous `## [Unreleased]` ; `/python-release` les fige en un bloc de version daté et incrémente la source de version (`config.py` `APP_VERSION`, source unique). La version n'est jamais incrémentée en silence. Voir `rules/versioning.md`.

---

## Points de vigilance

- `.claude/design-system.md` (v2.0) et `.claude/layout.md` (v4.1) sont la **source de vérité unique** — ne pas les dupliquer ni modifier sans bump de version. La composition portée par `layout.md` est un défaut modifiable (retenue validée en Phase 3) ; le skin de `design-system.md` reste contraignant.
- Les couleurs d'icônes Lucide sont dans `config.py` (`ICON_COLORS`), consommées par `utils/icons.py`, pas dans QSS (contrainte technique).
- Le contrat (`docs/specs/04-architect.md`) est verrouillé. Tout changement structurel passe par `/python-add-feature` ou le protocole de déclaration d'écart.
- `/python-load-project`, `/python-generate-readme`, `/python-add-feature`, `/python-trace-feature`, `/python-fix-issue`, `/python-refactor-code`, `/python-migrate-design`, `/python-release`, `/python-run-tests` s'invoquent depuis la racine du projet cible.
- `build.spec` est versionné (non gitignoré) si packaging Phase 1 Q7 = Oui.
- Toutes les commandes shell des skills sont compatibles Windows PowerShell.
