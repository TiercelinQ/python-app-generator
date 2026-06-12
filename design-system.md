# Design System — v1.0

> Référence contraignante pour toutes les applications Python/PyQt6.
> Usage : applications desktop Windows, usage personnel et professionnel.
> Indissociable de `layout.md`.

---

## 1. TYPOGRAPHIE

| Token         | Valeur   | Usage                         |
| ------------- | -------- | ----------------------------- |
| `font-family` | Segoe UI | Toutes les applications       |
| `xs`          | 12px     | Statusbar, labels secondaires |
| `sm`          | 14px     | Labels, sous-titres, corps    |
| `base`        | 16px     | Texte principal, navigation   |
| `lg`          | 18px     | Titres de section secondaires |
| `2xl`         | 24px     | Titres de section principaux  |
| `normal`      | 400      | Corps, descriptions           |
| `medium`      | 500      | Labels, items navigation      |
| `semibold`    | 600      | Titres, en-têtes              |
| `bold`        | 700      | Titres principaux             |

---

## 2. COULEURS

### Mode clair

| Token           | Valeur  | Usage                          |
| --------------- | ------- | ------------------------------ |
| `bg`            | #FFFFFF | Fond principal, topbar         |
| `bg-subtle`     | #F9FAFB | Fond topbar, zones secondaires |
| `bg-muted`      | #F3F4F6 | Statusbar, hover, alternance   |
| `bg-elevated`   | #FFFFFF | Drawer, modales                |
| `text`          | #111827 | Texte principal                |
| `text-subtle`   | #6B7280 | Texte secondaire, sous-titres  |
| `text-muted`    | #9CA3AF | Texte désactivé, statusbar     |
| `border`        | #E5E7EB | Bordures standard              |
| `border-subtle` | #F3F4F6 | Séparateurs discrets           |
| `border-strong` | #D1D5DB | En-têtes tableau               |

### Mode sombre

| Token           | Valeur  | Usage                  |
| --------------- | ------- | ---------------------- |
| `bg`            | #111827 | Fond principal, topbar |
| `bg-subtle`     | #1F2937 | Zones secondaires      |
| `bg-muted`      | #1F2937 | Statusbar, hover       |
| `bg-elevated`   | #374151 | Drawer, modales        |
| `text`          | #F9FAFB | Texte principal        |
| `text-subtle`   | #9CA3AF | Texte secondaire       |
| `text-muted`    | #6B7280 | Texte désactivé        |
| `border`        | #374151 | Bordures standard      |
| `border-subtle` | #1F2937 | Séparateurs discrets   |
| `border-strong` | #4B5563 | En-têtes tableau       |

### Couleur primaire — Slate Blue

| Token         | Clair   | Sombre  |
| ------------- | ------- | ------- |
| `primary-50`  | #EEF2FF | —       |
| `primary-400` | —       | #818CF8 |
| `primary-600` | #4F46E5 | —       |
| `primary-900` | —       | #312E81 |

> Modification : remplacer ces 4 valeurs suffit à changer la couleur primaire sur toute l'application.

### Couleurs sémantiques

| Token         | Clair   | Sombre  | Usage                  |
| ------------- | ------- | ------- | ---------------------- |
| `success-50`  | #F0FDF4 | —       | Fond toast succès      |
| `success-600` | #16A34A | #4ADE80 | Bordure, icône succès  |
| `warning-50`  | #FFFBEB | —       | Fond toast warning     |
| `warning-600` | #D97706 | #FCD34D | Bordure, icône warning |
| `danger-50`   | #FFF1F2 | —       | Fond toast danger      |
| `danger-600`  | #DC2626 | #F87171 | Bordure, icône danger  |
| `info-50`     | #EFF6FF | —       | Fond toast info        |
| `info-600`    | #2563EB | #60A5FA | Bordure, icône info    |

### Palette graphiques / visualisation

| Token           | Valeur        |
| --------------- | ------------- |
| `chart-primary` | `primary-600` |
| `chart-success` | `success-600` |
| `chart-warning` | `warning-600` |
| `chart-danger`  | `danger-600`  |
| `chart-info`    | `info-600`    |

---

## 3. ESPACEMENTS

| Token       | Valeur | Usage                     |
| ----------- | ------ | ------------------------- |
| `spacing-1` | 4px    | Micro-espacement          |
| `spacing-2` | 8px    | Padding interne compact   |
| `spacing-3` | 12px   | Padding standard          |
| `spacing-4` | 16px   | Espacement entre éléments |
| `spacing-6` | 24px   | Padding contenu principal |
| `spacing-8` | 32px   | Séparations majeures      |

---

## 4. TAILLES COMPOSANTS

### Tailles fixes (ancrages visuels globaux)

| Token              | Valeur | Usage                      |
| ------------------ | ------ | -------------------------- |
| `topbar-height`    | 48px   | Hauteur topbar             |
| `statusbar-height` | 28px   | Hauteur statusbar          |
| `drawer-width`     | 320px  | Largeur drawer droit       |
| `content-xl`       | 1024px | Largeur max contenu centré |
| `icon-sm`          | 16px   | Icône petite               |
| `icon-md`          | 20px   | Icône standard             |
| `icon-lg`          | 24px   | Icône navigation / topbar  |

### Tailles dynamiques — principe général

**Règle** : aucun composant n'a de hauteur ou largeur fixe sauf exception documentée ci-dessus. Les dimensions résultent du contenu + padding.

| Composant         | Largeur                                    | Hauteur                    | Exception                                     |
| ----------------- | ------------------------------------------ | -------------------------- | --------------------------------------------- |
| Bouton            | contenu + padding horizontal               | contenu + padding vertical | groupe aligné : uniformisée sur le plus large |
| Champ de saisie   | étire dans son conteneur (`setSizePolicy`) | contenu + padding vertical | —                                             |
| Colonne tableau   | contenu (`resizeColumnsToContents`)        | —                          | colonne actions : fixe                        |
| Onglet topbar     | label + padding horizontal                 | `topbar-height`            | —                                             |
| Label             | contenu, wrap si contrainte                | contenu                    | —                                             |
| Menu déroulant    | item le plus long                          | contenu                    | —                                             |
| Dialogue / modale | contenu                                    | contenu                    | min-width conseillée par contexte             |
| Item QTreeView    | contenu + indentation                      | padding vertical           | —                                             |
| Toast             | —                                          | contenu multi-ligne        | largeur fixe 320px                            |

---

## 5. FORME & OMBRES

| Token    | Valeur                      |
| -------- | --------------------------- |
| `radius` | 0px — flat design strict    |
| `shadow` | aucune — flat design strict |

---

## 6. TRANSITIONS

| Token                | Valeur     | Usage                   |
| -------------------- | ---------- | ----------------------- |
| `transition-default` | 150ms ease | États hover, focus      |
| `transition-slow`    | 250ms ease | Panels, drawer, onglets |

---

## 7. FOCUS

| Token        | Valeur                              |
| ------------ | ----------------------------------- |
| `focus-ring` | 2px solid `primary-600`, offset 2px |

---

## 8. ÉTATS DES COMPOSANTS INTERACTIFS

Applicable à tous les boutons, onglets, items cliquables :

| État                   | Règle                                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| `default`              | Style de base défini par le composant                                                             |
| `hover`                | Fond `bg-muted`, transition `transition-default`                                                  |
| `active` / sélectionné | Fond `primary-50`, texte `primary-600` (clair) / fond `primary-900`, texte `primary-400` (sombre) |
| `disabled`             | Opacité 40%, non interactif                                                                       |
| `focus`                | `focus-ring` visible                                                                              |

---

## 9. BOUTONS

| Variante   | Fond          | Texte         | Bordure      |
| ---------- | ------------- | ------------- | ------------ |
| Primaire   | `primary-600` | #FFFFFF       | aucune       |
| Secondaire | transparent   | `text`        | 1px `border` |
| Danger     | `danger-600`  | #FFFFFF       | aucune       |
| Ghost      | transparent   | `text-subtle` | aucune       |

**Dimensionnement dynamique** — la taille résulte du contenu + padding :

| Taille        | Padding vertical   | Padding horizontal | Police                 |
| ------------- | ------------------ | ------------------ | ---------------------- |
| `sm`          | `spacing-1` (4px)  | `spacing-3` (12px) | `medium` `xs` (12px)   |
| `md` (défaut) | `spacing-2` (8px)  | `spacing-4` (16px) | `medium` `sm` (14px)   |
| `lg`          | `spacing-3` (12px) | `spacing-6` (24px) | `medium` `base` (16px) |

**Groupe de boutons alignés** : largeur uniformisée sur le bouton le plus large (`setMinimumWidth` sur tous).

---

## 10. ICÔNES — qtawesome

Bibliothèque : `qtawesome` (wrapping Font Awesome).
Les icônes sont des widgets Python colorés dynamiquement — elles ne passent pas par QSS.

**Règle** : toutes les couleurs d'icônes sont définies dans `config.py`, jamais en dur dans les views ou controllers.

```python
# config.py — exemple
ICON_COLORS = {
    "light": {
        "default":  "#6B7280",   # text-subtle
        "active":   "#4F46E5",   # primary-600
        "danger":   "#DC2626",   # danger-600
        "success":  "#16A34A",   # success-600
        "muted":    "#9CA3AF",   # text-muted
    },
    "dark": {
        "default":  "#9CA3AF",   # text-subtle
        "active":   "#818CF8",   # primary-400
        "danger":   "#F87171",   # danger-600
        "success":  "#4ADE80",   # success-600
        "muted":    "#6B7280",   # text-muted
    }
}
```

**Tailles** : utiliser les tokens `icon-sm` (16px), `icon-md` (20px), `icon-lg` (24px).

```python
# Utilisation dans une view
import qtawesome as qta
icon = qta.icon("fa6s.house", color=ICON_COLORS[theme]["default"], scale_factor=1.0)
```

**Changement de thème** : les icônes sont recréées lors du basculement thème — pas de mise à jour dynamique de couleur sur instance existante.

---

## 11. RÈGLES D'APPLICATION QSS

1. **Zéro valeur visuelle en dur dans le code Python.** Toute couleur, taille, police est dans `styles.qss`.
2. **Chaque widget stylé a un `objectName`** correspondant à une règle QSS nommée.
3. **Le mode sombre est géré par remplacement de la feuille QSS** complète, pas par surcharge partielle.
4. **Toute valeur dans `styles.qss` est tracée vers un token de ce fichier.** Un commentaire indique le token source.

```qss
/* Exemple — token : bg / text */
QMainWindow {
    background-color: #FFFFFF;
    color: #111827;
}
```
