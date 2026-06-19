---
name: python-p1-scoping
description: Phase 1 of the development cycle — scoping a new application (6 questions + full color palette choice), provisional calibration, and writing of the scoping spec.
model: sonnet
---

# /python-p1-scoping — Scoping

## Role
Project scoper — turn a vague idea into a bounded, validated scope.

## Goal
Lock the project parameters (DB, prefs, i18n, tests, packaging, palette) before any analysis.

## Deliverable
`docs/specs/01-scoping.md` (written in French) + on-screen summary.

---

## Instructions — Phase 1: Scoping

> If invoked directly (not routed from `/python-app`) without a destination folder set for this flow, first ask: `Où créer l'application ? (chemin du dossier de destination)`.

Ask the following 6 questions in **a single block** (in French). Each closed question carries a `(recommandé)` answer:

1. Objectif de l'application — description libre.
2. Base de données : SQLite / PostgreSQL / JSON / CSV / aucune ? (recommandé : SQLite si données structurées, sinon aucune)
3. Préférences persistantes entre sessions (thème, fenêtre…) ? Oui / Non (recommandé : Oui)
4. Internationalisation FR/EN activée pour ce projet ? Oui / Non — FR par défaut (recommandé : Non sauf besoin EN avéré)
5. Tests automatisés (pytest + pytest-qt) ? Oui / Non (recommandé : Oui pour usage pro)
6. Packaging .exe (PyInstaller — build.spec + script PowerShell) ? Oui / Non (recommandé : Non sauf distribution)

After receiving the answers, propose the **color palette**. A palette = 5 **light** roles (fond principal, fond secondaire, accent, texte, détails); the dark theme and all supporting tokens are derived (`design-system.md §2`).

Palette de couleurs pour ce projet (5 rôles, thème clair — le sombre est dérivé) :

A. Acier (par défaut) — fond #FFFFFF · 2nd #F9FAFB · accent #4682B4 · texte #111827 · détails #E5E7EB — professionnel, tech, sobre (recommandé)
B. Forêt — fond #FFFFFF · 2nd #F6F8F6 · accent #059669 · texte #14201A · détails #DCE5DF — naturel, calme, frais
C. Ardoise — fond #FFFFFF · 2nd #F8FAFC · accent #4F46E5 · texte #1E293B · détails #E2E8F0 — moderne, net, indigo
D. Ambre — fond #FFFDFB · 2nd #FBF6EF · accent #B45309 · texte #1C1917 · détails #ECE3D8 — chaleureux, artisanal
E. Rubis — fond #FFFFFF · 2nd #FAF7F7 · accent #BE123C · texte #1A1212 · détails #EAE0E1 — affirmé, élégant

F. Palette personnalisée — fournis 5 hex clairs : fond principal, fond secondaire, accent, texte, détails.

Palette rules (see `@rules/config.md` "Deriving the full palette" + `design-system.md §2`):

- Acier (default) is option A and the recommended default; the 4 other named palettes (B-E) and the custom option (F) are full palettes. The catalog values are canonical — do not improvise the named ones.
- From the 5 light roles, Claude **derives** and announces: supporting light tokens (`bg-muted`, `bg-elevated`, `text-subtle`, `text-muted`, `border-subtle`, `border-strong`), the 5 accent stops (`primary-50/400/700/800/900`), `onPrimary`, and the **whole dark theme** (lightness targets in `design-system.md §2`).
- Written to `styles_light.qss` + `styles_dark.qss` (neutrals) and `config.py` (`PRIMARY_*`, `ON_PRIMARY`, `ICON_COLORS`). Semantic colors stay fixed.
- **Contrast check (WCAG AA, non-blocking)**: compute text/bg, text-subtle/bg, accent/bg, onPrimary/accent; if a ratio fails AA, report it (`couleur — ratio — cible`) and ask the user to confirm or adjust before continuing.
- The global `design-system.md` stays unchanged. If A or no answer: default palette (values already known).

Then announce the **provisional** calibration:

Calibrage provisoire : [Petit | Moyen/Grand] — [N] lots (dont 1 lot tests si activé)
(Sera confirmé à la fin de la Phase 2, après comptage des fonctionnalités réelles.)

Apply the CALIBRATION table in `CLAUDE.md` (canonical source).

## Write the spec

Write `docs/specs/01-scoping.md` (in French) capturing: objective, DB, preferences, i18n, tests, packaging, the **palette** (name or custom; the 5 light roles + the derived dark theme + accent stops + onPrimary; semantic kept fixed) and the contrast-check result, validated libraries, and the provisional calibration. If `docs/specs/` does not exist yet, create it (it will live in the generated project root).

Chain immediately to Phase 2 (`/python-p2-featuring`).
