# Guide d'utilisation — Python App Generator

---

## Structure du projet

```
python-app-generator/
├── .claude/
│   ├── CLAUDE.md                              # Instructions core
│   ├── design-system.md                       # Référence visuelle contraignante (v1.1)
│   ├── layout.md                              # Référence layout contraignante (v2.1)
│   ├── rules/
│   │   ├── mvc.md                             # Séparation MVC, livraison par lots, nettoyage anomalies
│   │   ├── qss.md                             # Règles QSS, tokens light/dark, flat design
│   │   ├── errors.md                          # Protocole erreurs, toasts, sys.excepthook
│   │   ├── config.md                          # config.py, requirements, packaging, dérivation couleurs
│   │   ├── tests.md                           # pytest + pytest-qt, couverture par couche
│   │   ├── logging.md                         # logging stdlib + RotatingFileHandler
│   │   ├── i18n.md                            # Workflow .ts/.qm, pylupdate6 / lrelease
│   │   └── db.md                              # Migrations versionnées SQLite/PostgreSQL
│   └── skills/
│       ├── python-app/         /python-app        # Menu démarrage / reprise (4 options)
│       ├── phase1-cadrage/     /phase1-cadrage    # Cadrage — 6 questions + 1 hex couleur
│       ├── phase2-analyse/     /phase2-analyse    # Fiche besoins + calibrage figé
│       ├── phase3-layout/      /phase3-layout     # Proposition layout + personnalisation
│       ├── phase4-contrat/     /phase4-contrat    # Contrat architectural verrouillé
│       ├── phase5-developpement/ /phase5-...      # Livraison par lots (enchaînement auto)
│       ├── feature-add/        /feature-add       # Ajouter une feature à un projet livré
│       ├── charger-projet/     /charger-projet    # Chargement d'un projet existant
│       ├── generate-readme/    /generate-readme   # Génération README.md projet existant
│       ├── session/            /session           # Sauvegarde de session
│       ├── statut/             /statut            # État courant du projet
│       ├── contrat/            /contrat           # Arborescence du contrat validé
│       ├── memoriser/          /memoriser         # Persiste dans .claude/project-memory.md
├── .gitignore
├── GUIDE.md                                   # Ce fichier
└── README.md                                  # Présentation du repo GitHub
```

---

## Installation depuis GitHub

```bash
# Cloner le repo
git clone https://github.com/[utilisateur]/python-app-generator.git
cd python-app-generator
```

### Prérequis

```bash
# Claude Code CLI installé et connecté
claude --version

# Python 3.10+ (pour exécuter les apps générées)
python --version
```

### Démarrage

```bash
# Depuis le dossier python-app-generator/
claude
```

Claude Code détecte `.claude/CLAUDE.md` automatiquement. `design-system.md` et `layout.md`
sont dans `.claude/` et importés via `@` — chargés à chaque session.

### Activer la mémoire (une seule fois, par machine)

```
/config
→ Memory → Enable auto memory → On
```

Sans cette activation, `/memoriser` formule les notes mais ne les persiste pas entre sessions.

---

## Fichiers ignorés par git (.gitignore)

Les fichiers suivants sont exclus du repo — propres à chaque utilisateur et machine :

| Fichier / Dossier             | Raison                                    |
| ----------------------------- | ----------------------------------------- |
| `.claude/settings.local.json` | Permissions et hooks personnels           |
| `.claude/agent-memory/`       | Mémoire auto Claude Code — personnelle    |
| `claude-sessions/`            | Fichiers SESSION propres à chaque projet  |
| `preferences.json`            | Préférences utilisateur des apps générées |
| `*.db`                        | Données applicatives                      |
| `.venv/`                      | Environnement virtuel local               |

> **Note** : `.claude/settings.json` (sans `.local`) peut être commité si tu veux partager
> des permissions ou hooks communs à tous les utilisateurs du repo.

---

## Effort recommandé par modèle

| Skill                                                                                                                                                  | Modèle | Effort recommandé     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | --------------------- |
| `/python-app` · `/statut` · `/contrat` · `/session` · `/memoriser` · `/charger-projet`                                                                 | Haiku  | — (tâches mécaniques) |
| `/phase1-cadrage` · `/phase2-analyse` · `/phase3-layout` · `/phase4-contrat` · `/phase5-developpement` · `/feature-add` · `/generate-readme`           | Sonnet | `medium`              |

`high` : justifié pour la Phase 4 (contrat complexe) ou le débogage multi-fichiers.
Changer l'effort en session : `/effort medium` ou `/effort high`.

---

## Démarrer une nouvelle application

```
/python-app → 1
```

### Phase 1 — Cadrage

Claude pose 6 questions en un seul bloc :

1. Objectif de l'application
2. Base de données (SQLite / PostgreSQL / JSON / CSV / aucune)
3. Préférences persistantes entre sessions (Oui / Non)
4. Internationalisation FR/EN (Oui / Non)
5. Tests automatisés — pytest + pytest-qt (Oui / Non — recommandé Oui pour usage pro)
6. Packaging .exe via PyInstaller (Oui / Non)

Puis propose 3 couleurs primaires adaptées au contexte + Slate Blue par défaut +
option personnalisée. L'utilisateur fournit uniquement `primary-600`, Claude dérive
`primary-50`, `primary-400`, `primary-900` via formule HSL déterministe.

Annonce un calibrage **provisoire** (sera figé après Phase 2) :

| Taille        | Lots (sans tests) | Lots (avec tests) |
| ------------- | ----------------- | ----------------- |
| Petit         | 3                 | 4                 |
| Moyen / Grand | 4                 | 5                 |

### Phase 2 — Analyse des besoins

Fiche structurée : objectif, fonctionnalités retenues, hors périmètre, contraintes techniques.
**Le calibrage est confirmé ici, à partir du compte réel de fonctionnalités.**
**→ Validation explicite requise avant Phase 3 — verrouille le nombre de lots.**

### Phase 3 — Proposition de layout

Claude propose une structure issue de `layout.md` puis pose les questions de personnalisation
en un seul bloc :

1. Position des onglets (gauche après logo / centrés)
2. Panneau secondaire (Drawer / Modale / Aucun)
3. Largeur du drawer si sélectionné (fixe 320px / fixe personnalisée / dynamique)
   ou taille de la modale si sélectionnée (fixe / dynamique)
4. Disposition interne de la modale si sélectionnée :
   - Header + contenu + footer
   - Header + 2 colonnes + footer
   - Header + contenu (sans footer)
   - Autre → Claude pose 3 questions pour aider à choisir, propose 2 dispositions avec recommandation
5. Emplacement des toasts (haut-droit par défaut, 5 autres positions disponibles)

Produit une synthèse complète du layout validé.
**→ Validation explicite requise avant Phase 4.**

### Phase 4 — Contrat architectural

Arborescence complète + rôle de chaque fichier + tableau tokens → règles QSS.
**→ Verrouillé après validation. Tout écart impose : arrêt → déclaration → validation.**

### Phase 5 — Développement par lots

Claude crée les dossiers et écrit les fichiers directement sur le disque — aucune action manuelle requise.
Format d'annonce : `📦 Lot N/[total] — [contenu]`
Enchaînement automatique entre les lots sans confirmation.

**Contenu par taille de projet — sans tests (Q5 = Non) :**

| Taille               | Lot 1                   | Lot 2                     | Lot 3                                                    | Lot 4                                                    |
| -------------------- | ----------------------- | ------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| Petit (3 lots)       | `config.py` + `models/` | `views/` + `controllers/` | `main.py` + `utils/` + `styles_*.qss` + `requirements.txt` | —                                                          |
| Moyen/Grand (4 lots) | `config.py` + `models/` | `views/`                  | `controllers/`                                             | `main.py` + `utils/` + `styles_*.qss` + `requirements.txt` |

**Contenu par taille de projet — avec tests (Q5 = Oui) :**

| Taille               | Lot 1                   | Lot 2                     | Lot 3                                                    | Lot 4                                                    | Lot 5                                                    |
| -------------------- | ----------------------- | ------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| Petit (4 lots)       | `config.py` + `models/` | `views/` + `controllers/` | `main.py` + `utils/` + `styles_*.qss` + `requirements.txt` | `tests/` + `requirements-dev.txt`                          | —                                                          |
| Moyen/Grand (5 lots) | `config.py` + `models/` | `views/`                  | `controllers/`                                             | `main.py` + `utils/` + `styles_*.qss` + `requirements.txt` | `tests/` + `requirements-dev.txt`                          |

**Dernier lot applicatif — livrables supplémentaires obligatoires :**

- Instructions d'installation (venv, pip, lancement)
- `README.md` écrit automatiquement à la racine du projet

**Lot tests — uniquement si Q5 = Oui :**

- `tests/` complet (miroir de la structure source)
- `requirements-dev.txt` (`pytest`, `pytest-qt`)
- Instructions `pytest` ajoutées au README

> **Note** : Claude Code demandera la permission d'exécuter Bash la première fois.
> Accepter pour tous les appels du projet pour ne pas être interrompu à chaque fichier.

---

## Reprendre une session existante

### Sauvegarder en fin de session

```
/session
```

Claude crée automatiquement le dossier `claude-sessions/` (s'il n'existe pas) et écrit
le fichier `SESSION_NomApp_SN.md` dedans.

### Reprendre

```
/python-app → 2
```

Claude demande le chemin du fichier SESSION, le lit automatiquement et reprend
sans re-poser les questions résolues.

```
ex: C:\projets\mon-app\claude-sessions\SESSION_MonApp_S1.md
```

---

## Travailler sur un projet existant (Phase 5 terminée)

Le `.claude/` doit être présent à la racine du projet. Si ce n'est pas le cas :

```bash
# Copier le .claude/ dans le projet existant (Windows)
xcopy /E /I python-app-generator\.claude mon-projet\.claude
```

Puis lancer Claude Code depuis la racine du projet :

```bash
cd mon-projet\
claude
```

**Projet avec README.md :**

```
/charger-projet
```

Claude lit `README.md`, confirme la prise en charge et applique toutes les règles.

**Projet sans README.md :**

```
/generate-readme
```

Claude analyse le code source et génère `README.md` automatiquement.

---

## Gestion des anomalies et mémoire

### Résolution d'anomalie

Après chaque correction, Claude produit :

```
Anomalie résolue. Éléments à retirer des tentatives précédentes :
Fichier [nom] : [lignes / blocs à supprimer]
```

Puis propose : `Veux-tu mémoriser ce point ? /memoriser`

### /memoriser

```
/memoriser
```

Claude demande ce qu'il faut retenir :

- A. Erreur à ne plus reproduire
- B. Décision structurante
- C. Préférence de génération
- D. Autre

Consigne une note datée et catégorisée dans `~/.claude/agent-memory/`.
Disponible dans toutes les sessions suivantes sur ce projet.

> La mémoire est stockée localement sur ta machine — elle n'est pas commitée dans le repo.

---

## Commandes de référence

| Commande                | Modèle | Action                                               |
| ----------------------- | ------ | ---------------------------------------------------- |
| `/python-app`           | Haiku  | Menu démarrage / reprise (4 options)                 |
| `/phase1-cadrage`       | Sonnet | Cadrage — 6 questions + couleur primaire             |
| `/phase2-analyse`       | Sonnet | Fiche besoins + calibrage figé                       |
| `/phase3-layout`        | Sonnet | Proposition layout + personnalisation                |
| `/phase4-contrat`       | Sonnet | Contrat architectural verrouillé                     |
| `/phase5-developpement` | Sonnet | Livraison par lots — enchaînement automatique        |
| `/feature-add`          | Sonnet | Ajouter une feature à un projet livré                |
| `/charger-projet`       | Haiku  | Charger un projet existant depuis son README.md      |
| `/generate-readme`      | Sonnet | Générer README.md d'un projet existant               |
| `/session`              | Haiku  | Sauvegarder la session dans `claude-sessions/`       |
| `/statut`               | Haiku  | État courant (phase, lot, décisions, points ouverts) |
| `/contrat`              | Haiku  | Arborescence du contrat architectural validé         |
| `/memoriser`            | Haiku  | Persister dans `.claude/project-memory.md`           |

---

## Structure d'une application générée

```
mon-app/
├── main.py                        # Point d'entrée
├── config.py                      # Constantes, PRIMARY_*, ICON_COLORS
├── requirements.txt
├── README.md                      # Généré automatiquement en fin de Phase 5
├── preferences.json               # Généré au premier lancement (si activé)
├── claude-sessions/               # Fichiers SESSION (gitignorés)
├── models/
│   ├── __init__.py
│   ├── exceptions.py              # Exceptions métier nommées
│   └── [entite]_model.py
├── views/
│   ├── __init__.py
│   ├── main_window.py             # Fenêtre principale, topbar, layout global
│   ├── toast_manager.py           # Toasts (position, animation, durées)
│   └── [entite]_view.py
├── controllers/
│   ├── __init__.py
│   └── [entite]_controller.py
├── utils/
│   └── helpers.py                 # Fonctions pures (formatage, JSON, validation)
└── resources/
    ├── styles_light.qss           # Thème clair — tous tokens design-system.md
    └── styles_dark.qss            # Thème sombre — tous tokens design-system.md

# Si tests activés en Phase 1 :
tests/
├── __init__.py
├── conftest.py                    # Fixtures partagées (qapp via pytest-qt auto)
├── test_helpers.py
├── models/
│   ├── __init__.py
│   ├── test_exceptions.py
│   └── test_[entite]_model.py
├── controllers/
│   ├── __init__.py
│   └── test_[entite]_controller.py
└── views/
    ├── __init__.py
    └── test_[entite]_view.py      # Smoke tests uniquement
requirements-dev.txt               # pytest>=8.0.0, pytest-qt>=4.4.0
```

---

## Ajouter une fonctionnalité à un projet livré

```
/feature-add
```

Workflow incrémental :
1. Cadrage léger (description + entité + type de modif + tests Oui/Non).
2. Diff du contrat architectural (fichiers créés / modifiés / supprimés).
3. Validation avant écriture.
4. Livraison en un seul lot.
5. Mise à jour `README.md` si stack ou dépendances changent.

Respect intégral des règles `@rules/*.md` — aucune modification non listée au diff.

---

## Logging, erreurs, base de données

### Logging (`@rules/logging.md`)

Toute app embarque `utils/logger.py` (config centralisée — `RotatingFileHandler` 1 MB × 5).
Logs dans `logs/[NomApp].log`, niveau `INFO` par défaut.

Activer le mode debug : variable d'environnement `[NOM_APP]_DEBUG=1`.

### Erreurs non capturées (`@rules/errors.md`)

`sys.excepthook` installé dans `main.py` → log critical + toast `danger` automatique.
Pas de crash silencieux en mode `--windowed`.

### Migrations DB (`@rules/db.md`)

`config.DB_SCHEMA_VERSION` + `models/migrations.py` avec dict `MIGRATIONS[version]`.
Appliquées au démarrage avant la `MainWindow`. Pas de rollback automatique.

---

## Tests automatisés

Activés via la **Q5 de la Phase 1** (recommandé : Oui pour usage pro).

### Stack

- `pytest >= 8.0`
- `pytest-qt >= 4.4` (smoke tests Views)
- `unittest.mock` (stdlib) pour les mocks

### Structure

`tests/` miroir de la structure source — un fichier de test par module source.
Détails complets et patterns : `.claude/rules/tests.md`.

### Couverture par défaut

| Couche                 | Cible                                                      |
| ---------------------- | ---------------------------------------------------------- |
| `models/`              | Logique métier complète, exceptions, edge cases            |
| `models/exceptions.py` | Smoke isinstance                                           |
| `controllers/`         | Wiring + try/except (model mocké → vérif `show_toast`)     |
| `utils/helpers.py`     | 100% lignes                                                |
| `views/`               | Smoke uniquement (instanciation + `objectName` via qtbot)  |

### Lancement

```bash
pip install -r requirements-dev.txt
pytest                              # tous les tests
pytest tests/models/                # une couche
pytest -k validation                # filtre par nom
pytest -v                           # verbeux
```

---

## Points de vigilance

- `design-system.md` (v1.1) et `layout.md` (v2.1) sont dans `.claude/` — ne pas les déplacer ni modifier sans bump de version.
- Les couleurs d'icônes qtawesome sont dans `config.py`, pas dans QSS (contrainte technique qtawesome).
- Le contrat architectural (Phase 4) est verrouillé. Tout changement structurel passe par `/feature-add` ou le protocole de déclaration.
- `/charger-projet`, `/generate-readme` et `/feature-add` doivent être invoqués depuis la racine du projet cible.
- `.claude/project-memory.md` est commitable et partageable — `~/.claude/agent-memory/` reste local à la machine.
- `.claude/settings.local.json` est gitignorée — chaque utilisateur configure ses propres permissions locales.
- `build.spec` est **versionné** (non gitignoré) si packaging Phase 1 Q6 = Oui.
- Toutes les commandes shell utilisées par les skills sont compatibles Windows PowerShell — pas de Bash requis.
