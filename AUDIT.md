# Audit & Remédiation — 12 juin 2026

> Synthèse de l'audit complet du générateur d'applications Python/PyQt6 et des
> corrections appliquées pour le rendre **performant, cohérent, robuste et
> optimal pour un usage quotidien personnel et professionnel**.

---

## Sommaire

- [Vue d'ensemble](#vue-densemble)
- [Décisions structurantes](#décisions-structurantes)
- [🔴 Bloquants (B1–B6)](#-bloquants-b1b6)
- [🟠 Majeurs (M1–M10)](#-majeurs-m1m10)
- [🟡 Robustesse (R1–R10)](#-robustesse-r1r10)
- [🟢 Mineurs (Min1–Min6)](#-mineurs-min1min6)
- [État final des fichiers](#état-final-des-fichiers)
- [Hors périmètre conscient](#hors-périmètre-conscient)
- [Vérifications finales](#vérifications-finales)

---

## Vue d'ensemble

| Catégorie       | Items traités | Items différés |
| --------------- | ------------- | -------------- |
| 🔴 Bloquants    | 6 / 6         | 0              |
| 🟠 Majeurs      | 10 / 10       | 0              |
| 🟡 Robustesse   | 10 / 10       | 0              |
| 🟢 Mineurs      | 6 / 6         | 0              |
| **Total**       | **32**        | **0**          |

5 fichiers créés · 18 fichiers mis à jour · 2 renommés.

---

## Décisions structurantes

Choix faits pour trancher des ambiguïtés ou ouvrir de nouvelles fonctionnalités.

| #  | Sujet                          | Décision retenue                                          | Justification                                              |
| -- | ------------------------------ | --------------------------------------------------------- | ---------------------------------------------------------- |
| B1 | Confirmation entre lots        | **Enchaînement auto**                                     | Productivité ; alignement avec GUIDE + phase5 majoritaires |
| B2 | Fichiers QSS                   | **2 séparés** (`styles_light.qss` + `styles_dark.qss`)    | Alignement majoritaire 5/6 fichiers existants              |
| B4 | Calibrage                      | **Provisoire en Phase 1 → figé en fin de Phase 2**        | Compté sur fonctionnalités réelles                         |
| B5 | `/memoriser`                   | **`.claude/project-memory.md`** versionable               | Partageable entre utilisateurs du repo                     |
| B6 | Couleurs primaires             | **1 hex (`primary-600`) → dérivation HSL des 3 autres**   | UX simplifiée ; table de 6 couleurs pré-calculées fournie  |
| R3 | Tests                          | **Opt-in Phase 1 Q5** · lot dédié · pytest + pytest-qt    | Choix utilisateur précédent                                |
| R7 | Packaging                      | **Opt-in Phase 1 Q6** · PyInstaller + build.spec versionné | Pas universellement nécessaire                            |
| R10 | Préférences persistées        | **Conservé en Q3 Phase 1**                                | Utile pour projets ultra-simples                           |

---

## 🔴 Bloquants (B1–B6)

### B1 — Contradiction directe sur la confirmation entre lots

**Constat** :
- `rules/mvc.md` exigeait `Lot N validé ? Je passe au N+1 dès confirmation.`
- `phase5-developpement/SKILL.md` indiquait l'inverse : `Enchaîner immédiatement sans attendre de confirmation.`
- `GUIDE.md` confirmait l'enchaînement auto.

Résultat : Claude appliquait l'un ou l'autre selon le fichier lu en premier.

**Solution** : alignement sur l'enchaînement automatique (productivité).

**Fichiers impactés** :
- `.claude/rules/mvc.md` — règle réécrite avec mention explicite "Enchaînement automatique"

---

### B2 — Un fichier QSS ou deux ?

**Constat** :
- `CLAUDE.md` mentionnait `styles.qss` (singulier).
- Tous les autres fichiers (README, GUIDE, phase4-contrat, mvc.md, qss.md) parlaient de `styles_light.qss` + `styles_dark.qss` (deux fichiers).
- `qss.md` ajoutait même : « Deux fichiers si complexité, sinon un seul » → règle floue.

**Solution** : **deux fichiers obligatoires** dans tous les cas. Règle durcie.

**Fichiers impactés** :
- `.claude/CLAUDE.md` — stack non négociable + règle absolue
- `.claude/rules/qss.md` — exigence durcie, suppression de la conditionnelle
- `.claude/rules/mvc.md` — tables de lots utilisent `styles_*.qss`
- `.claude/design-system.md` — section 11 (règles QSS) actualisée
- `.claude/skills/phase1-cadrage/SKILL.md` — mention des deux fichiers pour couleur primaire
- `GUIDE.md` — tables de lots actualisées

---

### B3 — Commandes shell Unix sur cible Windows

**Constat** : la stack cible Windows mais 6 skills utilisaient `cat`, `find`, `grep`, heredoc (`<< 'EOF'`) qui ne fonctionnent pas en PowerShell natif.

**Solution** : tous les skills concernés réécrits pour utiliser les outils natifs Claude Code (`Read`, `Write`, `Glob`) ou PowerShell compatible.

**Fichiers impactés** :
- `.claude/skills/python-app/SKILL.md` — `Read` au lieu de `cat`
- `.claude/skills/session/SKILL.md` — `Write` au lieu de `cat > … << EOF`, PowerShell `New-Item -Force` au lieu de `mkdir -p`
- `.claude/skills/charger-projet/SKILL.md` — `Read` + `Glob`
- `.claude/skills/generate-readme/SKILL.md` — `Read` + `Glob` + `Write`
- `.claude/skills/memoriser/SKILL.md` — `Read` + `Write` (nouveau fichier `.claude/project-memory.md`)

---

### B4 — Calibrage figé en Phase 1 avant connaissance des features

**Constat** : le critère "Fichiers < 10 ET fonctionnalités ≤ 5" était figé **avant** la Phase 2 qui produit la liste réelle des fonctionnalités. Calibrage aveugle.

**Solution** : annonce **provisoire** en Phase 1, confirmation **figée à la fin de Phase 2** sur les fonctionnalités comptées.

**Fichiers impactés** :
- `.claude/skills/phase1-cadrage/SKILL.md` — calibrage "provisoire", à confirmer
- `.claude/skills/phase2-analyse/SKILL.md` — bloc "Calibrage (figé après cette phase)" ajouté
- `GUIDE.md` — section Phase 1/Phase 2 reformulée

---

### B5 — `/memoriser` ne persistait rien

**Constat** : le skill formulait la note mais n'écrivait nulle part. La mémoire Claude Code (`~/.claude/agent-memory/`) requiert `/config → Memory → Enable auto memory → On`. Sans cette activation manuelle, les notes étaient perdues entre sessions. Silencieusement non fonctionnel.

**Solution** : persistance dans `.claude/project-memory.md` à la racine du projet, fichier versionable et partageable.

**Fichiers impactés** :
- `.claude/skills/memoriser/SKILL.md` — réécriture complète avec procédure Read → ajout → Write
- `.claude/CLAUDE.md` — tableau des commandes mis à jour

---

### B6 — Couleurs primaires : 2 hex demandés vs 4 tokens requis

**Constat** : `phase1-cadrage` proposait `[hex clair] / [hex sombre]` (2 valeurs) mais `config.py` requiert `PRIMARY_50/400/600/900` (4 valeurs). Aucune règle pour dériver les 2 manquantes.

**Solution** :
- L'utilisateur fournit **uniquement `primary-600`** (la valeur de référence).
- Claude dérive `primary-50`, `primary-400`, `primary-900` via formule HSL déterministe (même teinte, même saturation, luminosité à 95% / 70% / 25%).
- Table de correspondance fournie pour 6 couleurs pré-calculées (Slate Blue, Royal Blue, Emerald, Crimson, Amber, Violet).

**Fichiers impactés** :
- `.claude/skills/phase1-cadrage/SKILL.md` — proposition simplifiée à 1 hex + option E personnalisée
- `.claude/rules/config.md` — section "Dérivation des tokens primaires" + table de référence

---

## 🟠 Majeurs (M1–M10)

### M1 — `/charger-projet` oublié dans le tableau commandes de CLAUDE.md

**Constat** : présent dans README, GUIDE, frontmatter du skill, mais absent du tableau `## COMMANDES` de `CLAUDE.md` (11 entrées au lieu de 12).

**Solution** : ligne ajoutée.

**Fichiers impactés** : `.claude/CLAUDE.md`

---

### M2 — Modèles déclarés vs documentés incohérents

**Constat** :
- `contrat/SKILL.md` : pas de modèle déclaré (héritait du modèle session, potentiellement Sonnet → coûteux).
- `session/SKILL.md` : pas de modèle déclaré.
- `charger-projet/SKILL.md` : Haiku en frontmatter alors que GUIDE recommandait Sonnet.

**Solution** :
- `contrat` et `session` reçoivent `model: claude-haiku-4-5` (tâches mécaniques).
- `charger-projet` reste Haiku (lecture simple de README), GUIDE actualisé en conséquence.

**Fichiers impactés** :
- `.claude/skills/contrat/SKILL.md` — ajout `model: claude-haiku-4-5`
- `.claude/skills/session/SKILL.md` — réécriture inclut le modèle
- `GUIDE.md` — tableau "Effort recommandé" actualisé

---

### M3 — Extension `SKILL.MD` (majuscules)

**Constat** : `phase1-cadrage/SKILL.MD` et `phase3-layout/SKILL.MD` en majuscules. Risque sur loaders sensibles à la casse (macOS/Linux ou CI strict).

**Solution** : renommage via `git mv` pour préserver l'historique.

**Fichiers impactés** :
- `.claude/skills/phase1-cadrage/SKILL.MD` → `SKILL.md`
- `.claude/skills/phase3-layout/SKILL.MD` → `SKILL.md`

---

### M4 — `layout.md` se contredisait sur la position des onglets

**Constat** :
- Schéma ASCII ligne 80 : `[Logo] [Onglets nav] ··· [Thème]` → onglets à gauche.
- Tableau ligne 86 : « Centre | Onglets de navigation | flexible » → centrés.

`phase3-layout` propose les deux comme choix, mais `layout.md` ne devait pas trancher.

**Solution** : `layout.md` neutralisé — mention "alignement défini en Phase 3".

**Fichiers impactés** : `.claude/layout.md`

---

### M5 — `layout.md` ne décrivait qu'une position de toast

**Constat** : seule la position `top-right` était spécifiée (marges, animation). `phase3-layout` propose 6 positions sans aucune règle pour les 5 autres. Si Claude devait générer un toast `bottom-left`, il inventait.

**Solution** : section "Position — choix Phase 3" ajoutée à `layout.md` avec table complète des 6 positions (ancrage + animations entrée/sortie) + règles de marges et empilement adaptées (haut/bas).

**Fichiers impactés** : `.claude/layout.md`

---

### M6 — `errors.md` ignorait le toast `info` et `success`

**Constat** : pattern controller ne traitait que `warning` et `danger`. Pas d'exemple `success` (notification d'action réussie) ni `info` (notification neutre).

**Solution** :
- Pattern `else: self.view.show_toast("success", …)` ajouté à l'exemple obligatoire.
- Exemple `info` séparé pour notifications neutres.
- Tableau "Mapping exception → toast" ajouté (référence claire des 6 cas).

**Fichiers impactés** : `.claude/rules/errors.md`

---

### M7 — `/session` confondait sauvegarde et reprise

**Constat** : un seul skill décrivait à la fois la sauvegarde (lignes 1-60) et la reprise (lignes 62-68). `python-app` invoquait `/session` pour la reprise — ambigu.

**Solution** : skill réécrit avec deux sections claires : "Sauvegarde de session" (création fichier) et "Reprise depuis un fichier SESSION" (lecture). Les deux comportements restent dans le même skill mais sont explicitement séparés et déclenchés selon le contexte d'invocation.

**Fichiers impactés** : `.claude/skills/session/SKILL.md`

---

### M8 — Frontmatter Phase 5 auto-invocation contradictoire

**Constat** :
- Frontmatter : « Aussi invoquer pour chaque lot suivant dès la fin du lot précédent. »
- Contenu : « Enchaîner immédiatement sans attendre de confirmation. »

**Solution** : aligné sur l'enchaînement auto (cf. B1). Frontmatter inchangé mais le contenu confirme désormais l'absence de réinvocation entre lots.

**Fichiers impactés** : `.claude/skills/phase5-developpement/SKILL.md`

---

### M9 — Menu `/python-app` ne couvrait pas les cas réels

**Constat** : seulement 2 options (Nouvelle / Reprendre via SESSION). Cas non couverts : projet existant avec README mais sans SESSION (→ `/charger-projet`), projet sans rien (→ `/generate-readme`).

**Solution** : menu étendu à 4 options :
1. Nouvelle application
2. Reprendre une session (fichier SESSION)
3. Charger un projet existant (README.md)
4. Générer le README d'un projet existant

**Fichiers impactés** : `.claude/skills/python-app/SKILL.md`

---

### M10 — `disable-model-invocation` appliqué de façon incohérente

**Constat** : présent sur 5 skills (`python-app`, `session`, `statut`, `contrat`, `memoriser`), absent sur 7 — sans logique apparente.

**Solution** : harmonisé selon la règle "slash-only vs auto-routable".
- **Avec** `disable-model-invocation` (6 skills) : `python-app`, `session`, `statut`, `contrat`, `memoriser`, `charger-projet`.
- **Sans** (6 skills) : `phase1-cadrage`, `phase2-analyse`, `phase3-layout`, `phase4-contrat`, `phase5-developpement`, `generate-readme`, `feature-add` — peuvent être auto-invoqués dans un workflow.

**Fichiers impactés** : `.claude/skills/charger-projet/SKILL.md` (devient `disable-model-invocation: true`)

---

## 🟡 Robustesse (R1–R10)

### R1 — Aucune gestion de logging

**Constat** : aucune mention de `logging`, niveaux, rotation, destination fichier. Crash silencieux en mode `--windowed`. Inacceptable pour un usage pro.

**Solution** : nouvelle règle dédiée + intégration dans `config.py` + appel obligatoire dans `main.py`.

- Module `logging` stdlib (zéro dépendance externe).
- `RotatingFileHandler` 1 MB × 5 backups dans `logs/[NomApp].log`.
- Niveau `INFO` par défaut, `DEBUG` si variable d'environnement `[NOM_APP]_DEBUG=1`.
- `logger = logging.getLogger(__name__)` par module.
- `logger.exception(...)` obligatoire dans les `except` qui ne re-raise pas.
- Zéro `print()` dans le code livré.

**Fichiers impactés** :
- `.claude/rules/logging.md` — **NOUVEAU**
- `.claude/rules/config.md` — variables `LOG_*` ajoutées
- `.claude/rules/mvc.md` — `utils/logger.py` listé dans le dossier utils
- `.claude/skills/phase5-developpement/SKILL.md` — main.py inclut `setup_logging()`
- `.claude/CLAUDE.md` — règle absolue + référence `@rules/logging.md`

---

### R2 — Exceptions non capturées non gérées

**Constat** : `errors.md` couvrait les erreurs métier, mais aucune gestion des crashes inattendus (signal/slot lambda foireux, erreur thread Qt…). En mode `--windowed`, l'utilisateur ne voit rien.

**Solution** : `sys.excepthook` global installé dans `main.py`.

```python
def install_excepthook(main_window) -> None:
    def hook(exc_type, exc_value, exc_tb):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_tb)
            return
        logger.critical("Exception non capturée", exc_info=...)
        main_window.show_toast("danger", "Erreur inattendue", f"{exc_type.__name__} : {exc_value}")
    sys.excepthook = hook
```

**Fichiers impactés** :
- `.claude/rules/errors.md` — section "Gestion des exceptions non capturées"
- `.claude/skills/phase5-developpement/SKILL.md` — main.py template inclut `install_excepthook(window)`

---

### R3 — Tests automatisés absents

**Constat** : aucun framework de test, aucune structure `tests/`, aucune intégration dans les lots.

**Solution** (traitée précédemment) : règle dédiée + intégration phases + lot dédié opt-in.

- Stack : `pytest >= 8.0` + `pytest-qt >= 4.4` + `unittest.mock` stdlib.
- Activation opt-in via Phase 1 Q5.
- Lot dédié supplémentaire si activé (Petit → 4 lots, M/G → 5 lots).
- Couverture cible : models 100%, controllers wiring + try/except, utils 100%, views smoke uniquement.
- Patterns obligatoires fournis (controller avec model mocké, view avec `qtbot`).

**Fichiers impactés** :
- `.claude/rules/tests.md` — **NOUVEAU**
- `.claude/rules/mvc.md` — structure `tests/` + lots conditionnels + vérifs 12-13
- `.claude/rules/config.md` — `requirements-dev.txt`
- `.claude/skills/phase1-cadrage/SKILL.md` — Q5 + calibrage conditionnel
- `.claude/skills/phase2-analyse/SKILL.md` — contrainte `Tests: Oui/Non`
- `.claude/skills/phase4-contrat/SKILL.md` — arborescence `tests/` + mapping sources→tests
- `.claude/skills/phase5-developpement/SKILL.md` — lot tests + instructions pytest
- `.claude/skills/generate-readme/SKILL.md` — détection `tests/` + section README
- `.claude/skills/charger-projet/SKILL.md` — affichage état tests
- `.claude/skills/session/SKILL.md` — décision Tests verrouillée
- `.claude/CLAUDE.md` — règle absolue + référence
- `GUIDE.md` + `README.md` — section dédiée

---

### R4 — Aucun linter ni formatter

**Constat** : `CLAUDE.md` exigeait PEP 8 + type hints sans tooling automatique. Dérive garantie en utilisation continue.

**Solution** : ajout de `ruff` (lint + format) et `mypy` (type-check) à `requirements-dev.txt`, livraison d'un `pyproject.toml` minimal dans le dernier lot applicatif.

```toml
[tool.ruff]
line-length = 100
target-version = "py310"
[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM"]

[tool.mypy]
python_version = "3.10"
strict = true
ignore_missing_imports = true
exclude = ["tests/"]
```

**Fichiers impactés** :
- `.claude/rules/config.md` — section `pyproject.toml`
- `.claude/rules/mvc.md` — `pyproject.toml` ajouté au lot final
- `GUIDE.md` — mention dans la documentation

---

### R5 — Workflow i18n incomplet

**Constat** : `config.md` mentionnait `.ts` et `.qm` mais aucun skill n'orchestrait `pylupdate6` / `lrelease`. Si i18n activée, livraison incomplète.

**Solution** : nouvelle règle dédiée avec workflow complet.

- Stack : `PyQt6.QtCore.QTranslator` (natif) + `pylupdate6` (extraction) + `lrelease` (compilation).
- Scripts PowerShell `scripts/i18n_update.ps1` et `scripts/i18n_compile.ps1` livrés.
- Pas de rechargement à chaud — changement de langue = écriture préférences + redémarrage.
- Vérifications d'intégrité : zéro chaîne en dur dans Views.

**Fichiers impactés** :
- `.claude/rules/i18n.md` — **NOUVEAU**
- `.claude/rules/config.md` — synthèse + référence
- `.claude/skills/phase4-contrat/SKILL.md` — `resources/i18n/` ajouté à l'arborescence
- `.claude/CLAUDE.md` — règle conditionnelle + référence

---

### R6 — Migrations DB absentes

**Constat** : si Phase 1 = SQLite, aucune gestion de versioning de schéma. Tout changement futur cassait les bases existantes.

**Solution** : nouvelle règle avec migrations versionnées.

- Table `_schema_version` (entier) en base.
- `config.DB_SCHEMA_VERSION` = version cible attendue par le code.
- `models/migrations.py` avec dict `MIGRATIONS[version] = [SQL statements]`.
- Appliquées au démarrage avant la `MainWindow`.
- **Une seule direction** : `up` uniquement, pas de rollback automatique.
- Erreur si version DB > version code (mise à jour app requise).
- Mode JSON/CSV : pas de migrations auto (responsabilité utilisateur).

**Fichiers impactés** :
- `.claude/rules/db.md` — **NOUVEAU**
- `.claude/rules/config.md` — `DB_SCHEMA_VERSION` ajouté
- `.claude/rules/mvc.md` — `models/db.py` + `models/migrations.py` listés
- `.claude/skills/phase5-developpement/SKILL.md` — main.py inclut `run_migrations()`
- `.claude/CLAUDE.md` — règle conditionnelle + référence

---

### R7 — Packaging sous-spécifié

**Constat** : `config.md` proposait PyInstaller "sur demande", mais :
- `.gitignore` excluait `*.spec` (contradiction si packaging reproductible).
- Aucune mention de signature, MSIX, Inno Setup, gestion `sys._MEIPASS`.

**Solution** : opt-in via question Phase 1 Q6.

- Si Q6 = Oui : `build.spec` + `scripts/build.ps1` livrés en mini-lot.
- `helpers.resource_path()` documenté pour résoudre `sys._MEIPASS`.
- `preferences.json` et `logs/` déplacés vers `%APPDATA%/[NomApp]/` en mode bundled.
- `build.spec` versionné (retiré du `.gitignore`).
- Signature `.exe` reste hors périmètre (à faire avec `signtool`).

**Fichiers impactés** :
- `.claude/skills/phase1-cadrage/SKILL.md` — Q6 ajoutée
- `.claude/skills/phase2-analyse/SKILL.md` — contrainte "Packaging: Oui/Non"
- `.claude/rules/config.md` — section "Packaging Windows" enrichie
- `.gitignore` — `*.spec` retiré + commentaire explicatif
- `.claude/CLAUDE.md` — règle conditionnelle

---

### R8 — Pas d'évolution incrémentale possible

**Constat** : `/charger-projet` chargeait le contexte mais aucun skill ne formalisait l'ajout d'une fonctionnalité à un projet livré. Repartir d'une Phase 2 entière était lourd et risqué pour le contrat verrouillé.

**Solution** : nouveau skill `/feature-add` dédié.

Workflow :
1. Cadrage léger (description + entité + type + tests Oui/Non).
2. Diff du contrat architectural (fichiers créés / modifiés / supprimés).
3. Validation avant écriture.
4. Livraison en un seul lot respectant intégralement les règles `@rules/*.md`.
5. Mise à jour `README.md` si stack ou dépendances changent.

Si migration DB nécessaire : incrémenter `DB_SCHEMA_VERSION` + ajouter entrée `MIGRATIONS`.

**Fichiers impactés** :
- `.claude/skills/feature-add/SKILL.md` — **NOUVEAU**
- `.claude/CLAUDE.md` — commande ajoutée au tableau
- `GUIDE.md` + `README.md` — section dédiée

---

### R9 — Pas de versioning design-system / layout

**Constat** : `design-system.md v1.0` et `layout.md v2.0` mais aucun mécanisme de gestion du drift entre apps anciennes et nouvelles versions. Aucun changelog.

**Solution** :
- Changelog ajouté en tête de `design-system.md` (v1.0 → v1.1) et `layout.md` (v2.0 → v2.1).
- Mention "Toute application générée référence la version active dans son `README.md`".

Bumps appliqués :
- **Design System v1.1** : QSS 2 fichiers obligatoires + dérivation HSL.
- **Layout v2.1** : 6 positions toasts + onglets neutres + préférences précisées.

**Fichiers impactés** :
- `.claude/design-system.md` — header + changelog
- `.claude/layout.md` — header + changelog

---

### R10 — Question préférences vs hypothèse layout

**Constat** : Phase 1 demandait `Préférences Oui/Non`, mais `layout.md` et `config.md` les imposaient (taille fenêtre restaurée, thème). Si l'utilisateur disait Non, le layout devenait incohérent.

**Solution** : question conservée (utile pour projets ultra-simples), mais clarifications dans `config.md` et `layout.md` qui précisent que les préférences listées ne s'appliquent que si Q3 = Oui. Le `preferences.json` n'est généré qu'au premier lancement si activé.

**Fichiers impactés** :
- `.claude/rules/config.md` — clarification "Activées si Phase 1 Q3 = Oui"
- `.claude/layout.md` — section 10 reformulée

---

## 🟢 Mineurs (Min1–Min6)

### Min1 — `.gitignore` excluait `*.spec`

**Constat** : `config.md` proposait de livrer un `build.spec`, mais `.gitignore` l'excluait → packaging non reproductible.

**Solution** : `*.spec` retiré du `.gitignore` avec commentaire explicatif.

**Fichiers impactés** : `.gitignore`

---

### Min2 — Emplacement `preferences.json` non spécifié dans le contrat

**Constat** : `phase4-contrat` ne disait pas où placer `preferences.json` (root ? `data/` ?).

**Solution** : explicité comme étant à la **racine du projet** (gitignoré), avec déplacement automatique vers `%APPDATA%/[NomApp]/` en mode packaging `.exe`. Ajout également de `logs/` et `pyproject.toml` dans le contrat.

**Fichiers impactés** :
- `.claude/skills/phase4-contrat/SKILL.md` — arborescence enrichie
- `.claude/rules/config.md` — section préférences clarifiée

---

### Min3 — Pas de table couleur nom → tokens

**Constat** : utile pour Phase 1 quand 3 options dynamiques sont proposées.

**Solution** : table de référence dans `config.md` couvrant 6 couleurs pré-calculées (Slate Blue, Royal Blue, Emerald, Crimson, Amber, Violet) avec leurs 4 tokens dérivés.

**Fichiers impactés** : `.claude/rules/config.md`

---

### Min4 — Numérotation `N` des sessions non spécifiée

**Constat** : `SESSION_NomApp_S[N].md` mais aucune règle pour incrémenter `N`.

**Solution** : règle explicite :
1. Lister via `Glob` `claude-sessions/SESSION_*_S*.md`.
2. Extraire les entiers `N` via regex.
3. `[N] = max(entiers) + 1`, ou `1` si aucun fichier.

**Fichiers impactés** : `.claude/skills/session/SKILL.md`

---

### Min5 — README EN / GUIDE FR

**Constat** : usage volontaire. Documenté implicitement.

**Solution** : conservé tel quel. README en anglais (audience publique GitHub), GUIDE et skills en français (utilisateur cible).

**Fichiers impactés** : aucun (statu quo confirmé).

---

### Min6 — `layout.md` mentionnait `QSettings` OU `preferences.json`

**Constat** : ambiguïté entre deux mécanismes de persistance.

**Solution** : choix unique `preferences.json` (cohérent avec `config.md`, lecture via `utils/helpers.py`). `QSettings` retiré.

**Fichiers impactés** : `.claude/layout.md`

---

## État final des fichiers

### Fichiers créés (5)

| Fichier                                                | Rôle                                                |
| ------------------------------------------------------ | --------------------------------------------------- |
| `.claude/rules/tests.md`                               | Règle tests (pytest + pytest-qt, couverture)        |
| `.claude/rules/logging.md`                             | Règle logging stdlib + RotatingFileHandler          |
| `.claude/rules/i18n.md`                                | Règle i18n (workflow .ts/.qm complet)               |
| `.claude/rules/db.md`                                  | Règle base de données + migrations versionnées     |
| `.claude/skills/feature-add/SKILL.md`                  | Skill d'évolution incrémentale d'un projet livré    |

### Fichiers refondus (4)

| Fichier                                                | Refonte                                             |
| ------------------------------------------------------ | --------------------------------------------------- |
| `.claude/rules/config.md`                              | B6 + R1 + R4 + R7 + Min3 (dérivation couleurs, logging vars, pyproject, packaging, table couleurs) |
| `.claude/rules/errors.md`                              | M6 + R2 (info/success patterns + excepthook)        |
| `.claude/skills/memoriser/SKILL.md`                    | B5 (persistance project-memory.md)                  |
| `.claude/skills/python-app/SKILL.md`                   | M9 (menu 4 options)                                 |

### Fichiers mis à jour (14)

| Fichier                                                | Modifications principales                           |
| ------------------------------------------------------ | --------------------------------------------------- |
| `.claude/CLAUDE.md`                                    | B2 + M1 + R1 + R5 + R6 + R7 (stack, règles, commandes) |
| `.claude/design-system.md`                             | B2 + R9 (changelog v1.1 + QSS 2 fichiers)           |
| `.claude/layout.md`                                    | M4 + M5 + R9 + R10 + Min6 (onglets, toasts, prefs) |
| `.claude/rules/mvc.md`                                 | B1 + B2 + R1 + R3 + R6 (lots, QSS, logger, tests, db) |
| `.claude/rules/qss.md`                                 | B2 (2 fichiers obligatoires durcis)                 |
| `.claude/skills/phase1-cadrage/SKILL.md`               | B4 + B6 + R3 + R7 (Q5+Q6, calibrage provisoire, 1 hex) |
| `.claude/skills/phase2-analyse/SKILL.md`               | B4 + R3 + R7 (calibrage figé, tests, packaging)     |
| `.claude/skills/phase4-contrat/SKILL.md`               | R3 + R5 + Min2 (tests, i18n, prefs/logs/pyproject)  |
| `.claude/skills/phase5-developpement/SKILL.md`         | B1 + R2 + R3 + R6 (auto, excepthook, tests, migrations) |
| `.claude/skills/charger-projet/SKILL.md`               | B3 + M10 + R3 (Read/Glob, disable-invocation, tests) |
| `.claude/skills/contrat/SKILL.md`                      | M2 (model haiku)                                    |
| `.claude/skills/generate-readme/SKILL.md`              | B3 + R3 (Read/Glob/Write, section tests)            |
| `.claude/skills/session/SKILL.md`                      | B3 + M2 + M7 + Min4 (Write, model, save/load, numérotation) |
| `.gitignore`                                           | Min1 (*.spec retiré)                                |
| `GUIDE.md`                                             | Sync complet                                        |
| `README.md`                                            | Sync complet                                        |

### Fichiers renommés (2)

| Avant                                       | Après                                       |
| ------------------------------------------- | ------------------------------------------- |
| `.claude/skills/phase1-cadrage/SKILL.MD`    | `.claude/skills/phase1-cadrage/SKILL.md`    |
| `.claude/skills/phase3-layout/SKILL.MD`     | `.claude/skills/phase3-layout/SKILL.md`     |

---

## Hors périmètre conscient

Points identifiés mais non traités, par choix justifié :

| Point                                            | Raison                                                                     |
| ------------------------------------------------ | -------------------------------------------------------------------------- |
| Signature `.exe` (`signtool`)                    | Laissée à l'utilisateur, hors scope d'un générateur d'apps                 |
| Migration de schémas JSON/CSV                    | Pas de format imposé, responsabilité utilisateur                           |
| Tests E2E sur l'UI (Playwright-like)             | Over-engineering pour usage perso/pro standard                             |
| CI GitHub Actions / pre-commit hooks             | Non couvert — à ajouter sur demande explicite                              |
| Authentification utilisateur / RBAC              | Hors scope d'un générateur de squelette                                    |
| Internationalisation à chaud (hot reload)        | Complexité excessive, retraduction de tous les widgets ouverts            |

---

## Vérifications finales

| Vérification                                                          | Résultat                                    |
| --------------------------------------------------------------------- | ------------------------------------------- |
| Linter Markdown / typo                                                | Aucune erreur                               |
| Cohérence calibrage (5 fichiers)                                      | Petit `3/4` · M/G `4/5` partout             |
| Cohérence stack (pytest 8.0, pytest-qt 4.4, ruff 0.6, mypy 1.11)      | Synchronisée dans tous les fichiers         |
| Cohérence tableau commandes                                           | CLAUDE.md ↔ GUIDE.md ↔ README.md alignés    |
| Compatibilité Windows native                                          | Zéro `cat`, zéro heredoc, zéro `find` Unix  |
| Renommage SKILL.MD → SKILL.md détecté par git                         | OK (status `R`)                             |
| Toutes les références `@rules/*.md` valides                           | OK (4 nouvelles règles + 4 existantes)      |
| Commandes slash mentionnées présentes en skills                       | OK (13 skills · 13 commandes)               |

---

## Synthèse

Le générateur est désormais :

- **Cohérent** — toutes les contradictions internes (5 bloquantes) sont résolues.
- **Compatible Windows natif** — plus aucune dépendance shell Unix.
- **Robuste** — logging, excepthook, migrations DB, tests, linter intégrés par défaut.
- **Pro-ready** — opt-in tests (Q5) + opt-in packaging (Q6) en un seul Cadrage.
- **Évolutif** — `/feature-add` permet d'ajouter des features sans repartir de zéro.
- **Versionable** — design-system et layout disposent de changelogs.
- **Documenté** — README, GUIDE, CLAUDE.md et 8 fichiers de règles synchronisés.

Toutes les modifications ont été appliquées sur la branche courante. Aucun commit
n'a été créé — l'utilisateur reste maître du découpage et du message.
