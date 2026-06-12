# Layout Système — v2.0

> Référence contraignante pour toutes les applications Python/PyQt6.
> Construit sur `design-system.md v1.0`. Les deux fichiers sont indissociables.

---

## 1. STRUCTURE GLOBALE

```
┌─────────────────────────────────────────────────────┐
│              TOPBAR (48px)                          │
│  [ Logo / Nom ]  [ Onglets nav ]  [ Thème ]        │
├─────────────────────────────────────────────────────┤
│                                                     │
│            CONTENU PRINCIPAL                        │
│            (zone scrollable)                        │
│                                                     │
├─────────────────────────────────────────────────────┤
│                STATUSBAR (28px)                     │
└─────────────────────────────────────────────────────┘
```

**Drawer droit** (optionnel, par-dessus le contenu) :

```
┌─────────────────────────────────────────────────────┐
│                     TOPBAR                          │
├───────────────────────────────┬─────────────────────┤
│                               │                     │
│       CONTENU PRINCIPAL       │  DRAWER (320px)     │
│       (réduit)                │  coulissant         │
│                               │                     │
├───────────────────────────────┴─────────────────────┤
│                   STATUSBAR                         │
└─────────────────────────────────────────────────────┘
```

**Toast** (superposé, coin haut-droit) :

```
┌─────────────────────────────────────────────────────┐
│                     TOPBAR              [ Toast 1 ] │
├─────────────────────────────────────────[ Toast 2 ]─┤
│                                                     │
│            CONTENU PRINCIPAL                        │
│                                                     │
├─────────────────────────────────────────────────────┤
│                   STATUSBAR                         │
└─────────────────────────────────────────────────────┘
```

---

## 2. FENÊTRE

| Token               | Valeur                       |
| ------------------- | ---------------------------- |
| `min-width`         | 1024px                       |
| `min-height`        | 768px                        |
| état au lancement   | restauré (position + taille) |
| thème au lancement  | suit le thème OS             |
| thème par défaut OS | clair                        |

---

## 3. TOPBAR

| Token              | Valeur                 |
| ------------------ | ---------------------- |
| hauteur            | `topbar-height` = 48px |
| fond mode clair    | `bg` = #FFFFFF         |
| fond mode sombre   | `bg` = #111827         |
| bordure bas        | 1px `border`           |
| padding horizontal | `spacing-4` = 16px     |

### Zones de la topbar (gauche → droite)

```
[ Logo / Nom app ]  [ Onglets navigation ]  ···  [ Thème ]
```

| Zone   | Contenu                         | Largeur     |
| ------ | ------------------------------- | ----------- |
| Gauche | Logo SVG 24px + nom application | fixe        |
| Centre | Onglets de navigation (QTabBar) | flexible    |
| Droite | Sélecteur thème clair/sombre    | fixe — 40px |

### Logo / Nom application

- Icône SVG `icon-lg` (24px) + label `semibold` `base` (16px).
- Couleur : `text`.
- Non cliquable.

### Onglets de navigation (QTabBar)

- Intégrés dans la topbar, alignés centre.
- Maximum 5 onglets visibles. Au-delà → menu déroulant `···`.
- Onglet actif : texte `primary-600` (clair) / `primary-400` (sombre), bordure bas 2px `primary-600` / `primary-400`.
- Onglet inactif : texte `text-subtle`, fond transparent.
- Hover : fond `bg-muted`, transition `transition-default`.
- Police : `medium` `sm` (14px).
- Hauteur onglet : `topbar-height` = 48px (pleine hauteur topbar).
- Padding horizontal par onglet : `spacing-4` = 16px.

### Sélecteur de thème

- Icône seule (soleil / lune), taille `icon-lg` = 24px.
- Tooltip obligatoire : "Passer en mode sombre" / "Passer en mode clair".
- Toggle instantané — persisté en préférences utilisateur.

---

## 4. ZONE DE CONTENU PRINCIPAL

| Token               | Valeur                         |
| ------------------- | ------------------------------ |
| fond mode clair     | `bg` = #FFFFFF                 |
| fond mode sombre    | `bg` = #111827                 |
| padding intérieur   | `spacing-6` = 24px             |
| scroll              | vertical — `QScrollArea`       |
| largeur max contenu | `content-xl` = 1024px (centré) |

### En-tête de section

```
[ Titre de la section ]   [ Sous-titre / description courte ]
```

- Titre : `bold` `2xl` (24px), couleur `text`.
- Sous-titre : `normal` `sm` (14px), couleur `text-subtle`.
- Margin bas : `spacing-6` = 24px avant le contenu.

---

## 5. TOAST

Remplace intégralement le bandeau inline. Aucun bandeau inline dans les applications.

| Token                   | Valeur                                                 |
| ----------------------- | ------------------------------------------------------ |
| position                | Coin haut-droit, superposé au contenu                  |
| largeur                 | 320px                                                  |
| margin depuis le bord   | `spacing-4` = 16px                                     |
| margin depuis la topbar | `spacing-4` = 16px                                     |
| espacement entre toasts | `spacing-2` = 8px                                      |
| empilement              | Vertical, file d'attente, sans chevauchement           |
| animation entrée        | Glissement depuis la droite, `transition-slow` = 250ms |
| animation sortie        | Fondu + glissement droite, `transition-slow` = 250ms   |

### Durées d'affichage

| Type      | Durée      | Fermeture manuelle  |
| --------- | ---------- | ------------------- |
| `success` | 4s         | Non                 |
| `info`    | 4s         | Non                 |
| `warning` | 6s         | Oui (×)             |
| `danger`  | persistant | Oui (×) obligatoire |

### Anatomie du toast

```
┌────────────────────────────────────┐
│ [icône]  Message principal     [×] │
│          Description optionnelle   │
└────────────────────────────────────┘
```

| Token              | Valeur                                       |
| ------------------ | -------------------------------------------- |
| padding            | `spacing-3` vertical, `spacing-4` horizontal |
| bordure gauche     | 4px couleur sémantique                       |
| fond               | fond sémantique (`*-50`)                     |
| police message     | `medium` `sm` (14px)                         |
| police description | `normal` `xs` (12px), `text-subtle`          |
| icône              | `icon-md` = 20px                             |

| Type      | Fond         | Bordure       | Icône          |
| --------- | ------------ | ------------- | -------------- |
| `success` | `success-50` | `success-600` | check-circle   |
| `warning` | `warning-50` | `warning-600` | alert-triangle |
| `danger`  | `danger-50`  | `danger-600`  | x-circle       |
| `info`    | `info-50`    | `info-600`    | info           |

---

## 6. DRAWER DROIT

| Token            | Valeur                                                 |
| ---------------- | ------------------------------------------------------ |
| largeur          | `drawer-width` = 320px                                 |
| animation        | glissement depuis la droite, `transition-slow` = 250ms |
| fond mode clair  | `bg-elevated` = #FFFFFF                                |
| fond mode sombre | `bg-elevated` = #374151                                |
| bordure gauche   | 1px `border`                                           |
| padding          | `spacing-6` = 24px                                     |
| overlay fond     | `text` opacité 40%                                     |

- Ouvert par action explicite uniquement. Jamais automatiquement.
- Fermeture : clic overlay, touche Échap, ou bouton × dans le drawer.
- En-tête drawer : titre `semibold` `lg` (18px) + bouton × aligné à droite.
- Contenu drawer : scrollable verticalement si dépassement.

---

## 7. STATUSBAR

| Token              | Valeur                    |
| ------------------ | ------------------------- |
| hauteur            | `statusbar-height` = 28px |
| fond mode clair    | `bg-muted` = #F3F4F6      |
| fond mode sombre   | `bg-muted` = #1F2937      |
| bordure haut       | 1px `border`              |
| padding horizontal | `spacing-4` = 16px        |
| police             | `normal` `xs` (12px)      |
| couleur texte      | `text-muted`              |

### Zones statusbar (gauche → droite)

```
[ Message statut ]  ···  [ Progression ]  [ Info contextuelle ]
```

| Zone   | Contenu                                                                   |
| ------ | ------------------------------------------------------------------------- |
| Gauche | Message statut courant ("Prêt", "Chargement…", "3 éléments sélectionnés") |
| Centre | `QProgressBar` compact (8px) — visible uniquement si opération en cours   |
| Droite | Info contextuelle fixe (nb enregistrements, version, connexion DB…)       |

---

## 8. COMPOSANTS RÉCURRENTS

### Tableau de données (QTableView)

- En-tête : fond `bg-subtle`, `semibold` `sm` (14px), `text-subtle`.
- Bordure en-tête bas : 2px `border-strong`.
- Ligne : hauteur dynamique (padding vertical `spacing-2` = 8px), bordure bas 1px `border-subtle`.
- Colonnes : largeur dynamique (`resizeColumnsToContents`). Exception : colonne actions — largeur fixe selon contenu.
- Ligne sélectionnée : fond `primary-50` / `primary-900` (sombre).
- Ligne hover : fond `bg-muted`.
- Alternance de lignes : désactivée (flat design).
- Pagination sous le tableau si > 50 lignes.

### Formulaire de saisie

- Labels au-dessus des champs, `medium` `sm` (14px), `text`.
- Champs : largeur étirée dans le conteneur (`setSizePolicy(Expanding, Fixed)`), hauteur dynamique (padding vertical `spacing-2` = 8px).
- Espacement entre champs : `spacing-4` = 16px.
- Champ en erreur : bordure 2px `danger-600` + message `danger-600` sous le champ, `xs` (12px).
- Actions formulaire : alignées à droite — Annuler (secondaire) + Valider (primaire), largeur dynamique selon label.

### Arborescence (QTreeView)

- Indentation par niveau : `spacing-4` = 16px.
- Icône expand/collapse : chevron, `icon-sm` = 16px, `text-muted`.
- Item hauteur : dynamique (padding vertical `spacing-1` = 4px).
- Item sélectionné : fond `primary-50` / `primary-900` (sombre).

### Graphiques / Visualisation

- Fond : transparent (hérite du contenu principal).
- Palette : `chart-primary`, `chart-success`, `chart-warning`, `chart-danger`, `chart-info`.
- Légende : `normal` `sm` (14px), `text-subtle`.
- Aucune ombre (flat design).

### Modale (QDialog)

```
┌─────────────────────────────────────┐
│  Titre de la modale             [×] │
├─────────────────────────────────────┤
│                                     │
│  Contenu (formulaire, texte…)       │
│                                     │
├─────────────────────────────────────┤
│              [ Annuler ] [ Valider ]│
└─────────────────────────────────────┘
```

| Token            | Valeur                             |
| ---------------- | ---------------------------------- |
| largeur          | dynamique selon contenu, min 480px |
| fond mode clair  | `bg` = #FFFFFF                     |
| fond mode sombre | `bg` = #111827                     |
| bordure          | 1px `border`                       |
| padding          | `spacing-6` = 24px                 |
| overlay fond     | `text` opacité 40%                 |

- Ouverte par action explicite uniquement.
- Fermeture : bouton ×, Annuler, touche Échap, ou clic overlay.
- En-tête : titre `semibold` `lg` (18px) + bouton × aligné à droite, bordure bas 1px `border-subtle`.
- Pied : actions alignées à droite — Annuler (secondaire) + Valider (primaire), bordure haut 1px `border-subtle`.
- Contenu : scrollable verticalement si dépassement.
- Zéro `QMessageBox` natif — utiliser `QDialog` stylé.

### Pagination

Affichée sous un `QTableView` contenant plus de 50 lignes.

```
[ ← ]  [ 1 ]  [ 2 ]  [ 3 ]  ···  [ 12 ]  [ → ]
                  Page 2 sur 12
```

| Token                   | Valeur                                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------------------- |
| position                | sous le tableau, alignée à droite                                                                 |
| espacement avec tableau | `spacing-4` = 16px                                                                                |
| bouton page             | dynamique selon numéro, padding `spacing-2` horizontal                                            |
| bouton actif            | fond `primary-50`, texte `primary-600` (clair) / fond `primary-900`, texte `primary-400` (sombre) |
| bouton inactif          | transparent, texte `text-subtle`                                                                  |
| bouton hover            | fond `bg-muted`                                                                                   |
| boutons ← →             | icônes `icon-sm` (16px), désactivés en première/dernière page                                     |
| label page              | `normal` `xs` (12px), `text-muted`, centré sous les boutons                                       |
| pages max visibles      | 5 numéros — ellipse `···` au-delà                                                                 |

---

## 9. NAVIGATION CLAVIER GLOBALE

| Raccourci           | Action                                 |
| ------------------- | -------------------------------------- |
| `Tab` / `Shift+Tab` | Navigation entre éléments interactifs  |
| `Enter` / `Espace`  | Activation bouton / item focusé        |
| `Échap`             | Ferme drawer / modale / dropdown actif |
| `Alt+1…9`           | Navigation directe vers onglet N       |
| `Ctrl+,`            | Ouvre Paramètres                       |

---

## 10. PRÉFÉRENCES PERSISTÉES

Fichier `preferences.json` ou `QSettings` :

| Préférence       | Valeur par défaut |
| ---------------- | ----------------- |
| thème            | système OS        |
| fenêtre taille   | 1280×800          |
| fenêtre position | centrée           |
| drawer état      | fermé             |

---

## 11. RÉFÉRENCE CROISÉE DESIGN SYSTEM

Ce fichier ne redéfinit pas les tokens — il les consomme. Toute valeur visuelle est tracée vers `design-system.md v1.0`.

| Besoin                     | Token                                          |
| -------------------------- | ---------------------------------------------- |
| Fond principal             | `bg`                                           |
| Fond zones secondaires     | `bg-subtle`                                    |
| Fond drawer                | `bg-elevated`                                  |
| Texte principal            | `text`                                         |
| Texte secondaire           | `text-subtle`                                  |
| Bordures                   | `border` / `border-subtle` / `border-strong`   |
| Couleur active / sélection | `primary-600` (clair) / `primary-400` (sombre) |
| Focus                      | `focus-ring` 2px offset 2px                    |
| Transitions panels         | `transition-slow` = 250ms                      |
| Transitions états          | `transition-default` = 150ms                   |
| Forme                      | `radius` = 0px (flat design)                   |
| Ombres                     | aucune (flat design)                           |
