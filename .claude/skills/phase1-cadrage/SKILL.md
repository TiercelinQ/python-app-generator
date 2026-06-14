---
name: phase1-cadrage
description: Phase 1 of the development cycle — scoping a new application (6 questions + primary color HSL derivation), provisional calibration, and writing of the scoping spec.
model: sonnet
---

# /phase1-cadrage — Scoping

## Role
Project scoper — turn a vague idea into a bounded, validated scope.

## Goal
Lock the project parameters (DB, prefs, i18n, tests, packaging, color) before any analysis.

## Deliverable
`docs/specs/01-cadrage.md` (written in French) + on-screen summary.

---

## Instructions — Phase 1: Scoping

Ask the following 6 questions in **a single block** (in French):

```
1. Objectif de l'application — description libre.
2. Base de données : SQLite / PostgreSQL / JSON / CSV / aucune ?
3. Préférences persistantes entre sessions (thème, fenêtre…) ? Oui / Non
4. Internationalisation FR/EN activée pour ce projet ? Oui / Non (FR par défaut si Non)
5. Tests automatisés (pytest + pytest-qt) ? Oui / Non — recommandé Oui pour usage pro
6. Packaging .exe (PyInstaller — build.spec + script PowerShell) ? Oui / Non
```

After receiving the answers, propose the primary color choice:

```
Couleur primaire pour ce projet (un seul hex `primary-600` suffit — Claude dérive les 3 autres) :

A. [Color 1] — primary-600 = [hex] — [character in 3 words]
B. [Color 2] — primary-600 = [hex] — [character in 3 words]
C. [Color 3] — primary-600 = [hex] — [character in 3 words]
D. Slate Blue  — primary-600 = #4F46E5 — professionnel, tech, sobre (défaut)
E. Personnalisé — fournir un hex `primary-600` (ex: #2563EB)
```

Color rules (see `@rules/config.md` "Deriving the primary tokens"):

- Propose 3 professional colors suited to the described application context.
- From the chosen `primary-600`, Claude **derives** automatically:
  - `primary-50`  = same hue, ~95% lightness (light selection bg)
  - `primary-400` = same hue, ~70% lightness (dark active text)
  - `primary-900` = same hue, ~25% lightness (dark selection bg)
- The 4 values are written to `config.py` (`PRIMARY_*`) and `styles_light.qss` / `styles_dark.qss`.
- The global `design-system.md` stays unchanged.
- If D or no answer: Slate Blue by default (4 values already known).

Then announce the **provisional** calibration:

```
Calibrage provisoire : [Petit | Moyen/Grand] — [N] lots (dont 1 lot tests si activé)
(Sera confirmé à la fin de la Phase 2, après comptage des fonctionnalités réelles.)
```

Apply the CALIBRATION table in `CLAUDE.md` (canonical source).

## Write the spec

Write `docs/specs/01-cadrage.md` (in French) capturing: objective, DB, preferences, i18n, tests, packaging, primary color (the 4 derived hex values), validated libraries, and the provisional calibration. If `docs/specs/` does not exist yet, create it (it will live in the generated project root).

Chain immediately to Phase 2 (`/phase2-analyse`).
