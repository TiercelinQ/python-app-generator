---
description: Phase 3 du cycle de développement — proposition de layout.
             Invoquer après validation de la Phase 2.
model: claude-sonnet-4-6
---

## Instructions — Phase 3 : Proposition de layout

Sur la base des fonctionnalités validées en Phase 2, proposer un layout issu de `layout.md`,
puis poser les questions de personnalisation en **un seul bloc**.

---

### Étape 1 — Proposition initiale

Produire :

```
## Layout proposé — [NOM_APP]

**Structure**
[Description de la disposition : topbar, onglets, contenu principal, statusbar]

**Onglets**
| Onglet | Contenu |
| ------ | ------- |
| …      | …       |

**Composants récurrents**
- [Tableau / Formulaire / Arborescence / Graphiques — selon les fonctionnalités]
```

---

### Étape 2 — Questions de personnalisation (un seul bloc)

Poser immédiatement après la proposition :

```
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
```

Afficher uniquement les questions pertinentes selon le contexte des fonctionnalités.
Si le projet n'a visiblement pas besoin de drawer ni de modale, ne pas poser les questions 3/4
mais mentionner l'absence de panneau secondaire dans la proposition.
La question 5 (toasts) est toujours posée.

Si l'utilisateur choisit D à la question 4 : poser 3 questions en un seul bloc pour l'aider à
définir la disposition :

```
Pour t'aider à choisir la disposition :

a. Quel est l'objectif principal de cette modale ?
   (ex: saisir un formulaire, afficher un détail, confirmer une action, visualiser un document…)

b. Y a-t-il des actions à effectuer depuis cette modale (boutons Valider / Annuler / Supprimer…) ?
   Oui / Non

c. Le contenu est-il homogène (un seul bloc) ou hétérogène (plusieurs sections distinctes) ?
   Homogène / Hétérogène — préciser les sections si hétérogène
```

Sur la base des réponses, proposer 2 dispositions adaptées avec une recommandation justifiée,
puis demander confirmation avant de passer à la synthèse.

---

### Étape 3 — Synthèse finale

Après réception des réponses, produire la synthèse complète :

```
## Layout validé — [NOM_APP]

**Topbar**
- Logo + nom : gauche
- Onglets : [gauche après logo | centrés]
- Toggle thème : droite
- Hauteur : 48px

**Onglets**
| Onglet | Contenu |
| ------ | ------- |
| …      | …       |

**Panneau secondaire** : [Drawer | Modale | Aucun]
- [Drawer] Largeur : [320px fixe | Xpx fixe | dynamique]
- [Modale] Taille : [X×Y fixe | dynamique]
- [Modale] Disposition : [description retenue]

**Composants récurrents**
- [liste]

**Toasts** : [emplacement retenu] · zéro bandeau inline

**Contraintes appliquées**
- Topbar 48px · Statusbar 28px · Fenêtre min 1024×768
- Drawer : ouvert sur action explicite, fermable via Échap / overlay / ×
- Position et taille fenêtre restaurées au relancement

→ Validation requise avant Phase 4.
  Confirmer ou lister les ajustements.
```

**Règle bloquante** : ne pas passer à Phase 4 tant que la validation n'est pas explicite.