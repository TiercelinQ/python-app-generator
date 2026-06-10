# Guide d'utilisation — Python App Generator

---

## Structure du projet

```
python-app-generator/
├── .claude/
│   ├── CLAUDE.md                              # Instructions core
│   ├── design-system.md                       # Référence visuelle contraignante
│   ├── layout.md                              # Référence layout contraignante
│   ├── rules/
│   │   ├── mvc.md                             # Séparation MVC, livraison par lots, nettoyage anomalies
│   │   ├── qss.md                             # Règles QSS, tokens light/dark, flat design
│   │   ├── errors.md                          # Protocole gestion des erreurs, toasts
│   │   └── config.md                          # Structure config.py, requirements.txt, i18n, packaging
│   └── skills/
│       ├── python-app/     /python-app        # Menu démarrage / reprise
│       ├── phase1-cadrage/ /phase1-cadrage    # Cadrage — 4 questions + couleur primaire
│       ├── phase2-analyse/ /phase2-analyse    # Fiche besoins structurée
│       ├── phase3-layout/  /phase3-layout     # Proposition layout + personnalisation
│       ├── phase4-contrat/ /phase4-contrat    # Contrat architectural verrouillé
│       ├── phase5-developpement/ /phase5-...  # Livraison par lots + README.md
│       ├── charger-projet/ /charger-projet    # Chargement d'un projet existant
│       ├── generate-readme/ /generate-readme  # Génération README.md projet existant
│       ├── session/        /session           # Sauvegarde de session
│       ├── statut/         /statut            # État courant du projet
│       ├── contrat/        /contrat           # Arborescence du contrat validé
│       ├── memoriser/      /memoriser         # Mémorisation erreurs / décisions
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

| Skill                                                                                                                                           | Modèle | Effort recommandé     |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | ------ | --------------------- |
| `/python-app` · `/statut` · `/contrat` · `/session` · `/memoriser`                                                                              | Haiku  | — (tâches mécaniques) |
| `/phase1-cadrage` · `/phase2-analyse` · `/phase3-layout` · `/phase4-contrat` · `/phase5-developpement` · `/charger-projet` · `/generate-readme` | Sonnet | `medium`              |

`high` : justifié pour la Phase 4 (contrat complexe) ou le débogage multi-fichiers.
Changer l'effort en session : `/effort medium` ou `/effort high`.

---

## Démarrer une nouvelle application

```
/python-app → 1
```

### Phase 1 — Cadrage

Claude pose 4 questions en un seul bloc :

1. Objectif de l'application
2. Base de données (SQLite / PostgreSQL / JSON / CSV / aucune)
3. Préférences persistantes entre sessions (Oui / Non)
4. Internationalisation FR/EN (Oui / Non)

Puis propose 3 couleurs primaires adaptées au contexte + l'option Slate Blue par défaut.
Annonce le calibrage (Petit : 3 lots / Moyen-Grand : 4 lots) — figé après cette phase.

### Phase 2 — Analyse des besoins

Fiche structurée : objectif, fonctionnalités retenues, hors périmètre, contraintes techniques.
**→ Validation explicite requise avant Phase 3.**

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

**Contenu par taille de projet :**

| Taille               | Lot 1                   | Lot 2                     | Lot 3                                                    | Lot 4                                                    |
| -------------------- | ----------------------- | ------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| Petit (3 lots)       | `config.py` + `models/` | `views/` + `controllers/` | `main.py` + `utils/` + `styles.qss` + `requirements.txt` | —                                                        |
| Moyen/Grand (4 lots) | `config.py` + `models/` | `views/`                  | `controllers/`                                           | `main.py` + `utils/` + `styles.qss` + `requirements.txt` |

**Dernier lot — livrables supplémentaires obligatoires :**

- Instructions d'installation (venv, pip, lancement)
- `README.md` écrit automatiquement à la racine du projet

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
| `/python-app`           | Haiku  | Menu démarrage / reprise                             |
| `/phase1-cadrage`       | Sonnet | Cadrage — 4 questions + couleur primaire             |
| `/phase2-analyse`       | Sonnet | Fiche besoins structurée                             |
| `/phase3-layout`        | Sonnet | Proposition layout + personnalisation                |
| `/phase4-contrat`       | Sonnet | Contrat architectural verrouillé                     |
| `/phase5-developpement` | Sonnet | Livraison par lots — fichiers écrits sur le disque   |
| `/charger-projet`       | Sonnet | Charger un projet existant depuis son README.md      |
| `/generate-readme`      | Sonnet | Générer README.md d'un projet existant               |
| `/session`              | Haiku  | Sauvegarder la session dans `claude-sessions/`       |
| `/statut`               | Haiku  | État courant (phase, lot, décisions, points ouverts) |
| `/contrat`              | Haiku  | Arborescence du contrat architectural validé         |
| `/memoriser`            | Haiku  | Mémoriser une erreur, décision ou préférence         |

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
```

---

## Points de vigilance

- `design-system.md` et `layout.md` sont dans `.claude/` — ne pas les déplacer ni modifier.
- Les couleurs d'icônes qtawesome sont dans `config.py`, pas dans QSS (contrainte technique qtawesome).
- Le contrat architectural (Phase 4) est verrouillé. Tout changement structurel impose le protocole de déclaration.
- `/charger-projet` et `/generate-readme` doivent être invoqués depuis la racine du projet cible.
- La mémoire (`~/.claude/agent-memory/`) est locale à ta machine — non commitée, non partagée.
- `.claude/settings.local.json` est gitignorée — chaque utilisateur configure ses propres permissions locales.
