---
name: python-p3-designing
description: Phase 3 of the development cycle — layout proposal from layout.md, grouped customization questions, validated synthesis written to the layout spec before Phase 4.
model: sonnet
---

# /python-p3-designing — Layout proposal

## Role
UI designer — map the validated features onto the binding layout system.

## Goal
Define the concrete layout (tabs, drawer/modal, toast position) within `layout.md` constraints.

## Deliverable
`docs/specs/03-designing.md` (written in French) + on-screen synthesis.

---

## Instructions — Phase 3: Layout proposal

**Read `design-system.md` and `layout.md` first** (no longer auto-imported).

Based on the features validated in Phase 2 (`docs/specs/02-featuring.md`), propose a layout drawn from `layout.md`, then ask the customization questions in **a single block**.

### Step 1 — Initial proposal

Produce (in French):

## Layout proposé — [NOM_APP]

**Structure**
[Description : topbar, onglets, contenu principal, statusbar]

**Onglets**
| Onglet | Contenu |
| ------ | ------- |
| …      | …       |

**Composants récurrents**
- [Tableau / Formulaire / Arborescence / Graphiques — selon les fonctionnalités]

### Step 2 — Customization questions (single block)

For each question, mark the option you recommend with `(recommandé)`, chosen from the validated feature context.

Quelques choix à confirmer :

1. Position des onglets dans la topbar :
   A. Après le logo et le nom (alignés à gauche)
   B. Centrés

2. Panneau secondaire : drawer ou modale ?
   A. Drawer (panneau latéral persistant)
   B. Modale (fenêtre superposée)
   C. Aucun

[Si A — Drawer :]
3. Largeur du drawer :
   A. Fixe 320px (défaut design-system.md)
   B. Fixe personnalisée — préciser la valeur
   C. Dynamique (s'adapte au contenu)

[Si B — Modale :]
3. Taille de la modale :
   A. Fixe — préciser largeur × hauteur
   B. Dynamique (s'adapte au contenu)

4. Disposition interne de la modale :
   A. Header + contenu principal + footer
   B. Header + 2 colonnes (contenu principal) + footer
   C. Header + contenu principal (sans footer)
   D. Autre — je ne sais pas, aide-moi à choisir

5. Emplacement des toasts :
   A. Haut-droit (défaut)
   B. Haut-gauche
   C. Haut-centre
   D. Bas-droit
   E. Bas-gauche
   F. Bas-centre

Show only the relevant questions for the feature context. If the project clearly needs no drawer or modal, skip questions 3/4 and note the absence of a secondary panel. Question 5 (toasts) is always asked.

If the user picks D on question 4: ask 3 questions in a single block to help define the layout:

Pour t'aider à choisir la disposition :

a. Quel est l'objectif principal de cette modale ?
b. Y a-t-il des actions à effectuer depuis cette modale ? Oui / Non
c. Le contenu est-il homogène (un seul bloc) ou hétérogène (plusieurs sections) ?

Based on the answers, propose 2 suited layouts with a justified recommendation, then confirm before the synthesis.

### Step 3 — Final synthesis

Produce the complete synthesis (in French): topbar, tabs, secondary panel, recurring components, toast position, applied constraints.

→ Validation requise avant Phase 4.
  Confirmer ou lister les ajustements.

**Blocking rule**: do not move to Phase 4 until validation is explicit.

## Write the spec

Once validated, write the synthesis to `docs/specs/03-designing.md` (in French).

Chain to `/python-p4-architect` after validation.
