---
description: Ajoute une fonctionnalité à un projet existant en respectant le contrat
             architectural verrouillé. Invoquer depuis la racine du projet cible,
             après /charger-projet ou sur un projet déjà chargé.
model: claude-sonnet-4-6
---

## Pré-requis

Le projet doit être chargé (`/charger-projet` exécuté en début de session, OU
README.md présent et lu).

Si aucun contrat n'est connu : interrompre et demander `/charger-projet`.

---

## Étape 1 — Cadrage léger de la fonctionnalité

Poser en un seul bloc :

```
Nouvelle fonctionnalité — quelques questions :

1. Description courte (1 phrase)
2. Entité métier impactée : [existante : liste] | nouvelle (à nommer)
3. Type de modification :
   A. Nouvelle entité (model + view + controller)
   B. Extension d'une entité existante
   C. Nouvelle vue partagée (sans nouveau model)
   D. Modification UI seule (QSS ou layout)
4. Tests à générer pour cette feature ? Oui / Non (déduit de la stack projet)
```

---

## Étape 2 — Diff du contrat architectural

Produire :

```
## Diff contrat — ajout : [nom feature]

### Fichiers créés
[liste]

### Fichiers modifiés
[liste avec nature : ajout méthode, ajout widget, ajout signal…]

### Fichiers tests créés (si Q4 = Oui)
[liste miroir]

### Impact sur design-system / layout
[aucun | nouveau composant à respecter dans les tokens existants]
```

→ Validation requise avant écriture.

---

## Étape 3 — Application — règles strictes

- Respecter intégralement `@rules/mvc.md`, `@rules/qss.md`, `@rules/errors.md`,
  `@rules/config.md`, `@rules/tests.md`, `@rules/logging.md`, `@rules/i18n.md`, `@rules/db.md`.
- Aucune modification non listée dans le diff validé.
- Aucune amélioration opportuniste du code adjacent.
- Si migration DB nécessaire : incrémenter `DB_SCHEMA_VERSION`, ajouter une entrée
  dans `MIGRATIONS` de `models/migrations.py`.
- Si chaîne UI ajoutée et i18n activée : mettre à jour `.ts` (rappeler à l'utilisateur
  de lancer `scripts/i18n_update.ps1`).
- Si nouveau widget stylé : ajouter règle QSS dans `styles_light.qss` ET `styles_dark.qss`.

---

## Étape 4 — Livraison

Format identique à Phase 5 — un seul lot pour la feature :

```
📦 Feature [nom] — [N fichiers]
```

Livrer chaque fichier créé/modifié en bloc complet.

Si tests demandés : livrer dans le même lot, à la fin.

---

## Étape 5 — Anomalie

Si l'utilisateur signale une anomalie après livraison, appliquer le protocole
de `@rules/mvc.md` (section "Résolution d'anomalie") puis proposer `/memoriser`.

---

## Vérification d'intégrité

1. Tous les fichiers créés/modifiés correspondent au diff validé en Étape 2.
2. Aucune régression dans les imports (les fichiers existants restent fonctionnels).
3. Si tests : `pytest` exit code 0 sur l'ensemble du projet (pas seulement les nouveaux).
4. Mise à jour `README.md` si la feature change la stack ou ajoute une dépendance.
