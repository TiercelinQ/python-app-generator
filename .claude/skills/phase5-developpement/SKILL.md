---
description: Phase 5 du cycle de développement — livraison du code par lots.
             Invoquer après validation du contrat architectural (Phase 4).
             Aussi invoquer pour chaque lot suivant dès la fin du lot précédent.
model: claude-sonnet-4-6
---

## Instructions — Phase 5 : Développement par lots

Référence livraison : `@rules/mvc.md` (section "Livraison par lots") — tables conditionnelles
selon la réponse à Q5 (tests activés ou non).

### Répertoire cible

Au début de la Phase 5, demander à l'utilisateur le répertoire racine du projet cible :

```
Répertoire de destination pour les fichiers ? (ex: C:\projets\MonApp)
```

Stocker ce chemin. Tous les fichiers sont écrits à cet emplacement via l'outil `Write`.
Créer les sous-dossiers nécessaires avant d'écrire les fichiers qu'ils contiennent.

### Avant chaque lot

Annoncer : `📦 Lot N/[total] — [contenu]`

Pour chaque fichier du lot : écrire le fichier directement sur disque via l'outil `Write`
à `[répertoire_cible]/[chemin_relatif_du_fichier]`. Contenu complet et autonome.

### Après chaque lot (sauf le dernier)

Enchaîner immédiatement sur le lot suivant sans attendre de confirmation.

### Lot tests — uniquement si Phase 1 Q5 = Oui

Annoncer : `📦 Lot [final]/[total] — tests/ + requirements-dev.txt`

Livrer dans cet ordre :
1. `tests/__init__.py`
2. `tests/conftest.py` (fixtures partagées projet, qapp auto via pytest-qt)
3. `tests/test_helpers.py`
4. `tests/models/__init__.py` + `tests/models/test_exceptions.py` + un `tests/models/test_*.py` par modèle
5. `tests/controllers/__init__.py` + un `tests/controllers/test_*.py` par controller (model mocké)
6. `tests/views/__init__.py` + un `tests/views/test_*.py` par view (smoke uniquement)
7. `requirements-dev.txt`

Respect strict de `@rules/tests.md` :
- Pattern controller mocké avec `unittest.mock.Mock`, vérification `view.show_toast.assert_called_*`.
- Pattern smoke view avec fixture `qtbot`, vérification `objectName` et widgets clés via `findChild`.
- Aucun `time.sleep`, aucun `assert True`, aucun accès réseau/DB de production.

Après livraison, ajouter aux instructions d'installation :

```
# 5. Installer les dépendances de test
pip install -r requirements-dev.txt

# 6. Lancer les tests
pytest

# 7. Cibler une couche
pytest tests/models/
```

### Dernier lot — fichiers obligatoires

**0. main.py — initialisations obligatoires (ordre strict) :**

```python
from utils.logger import setup_logging
from models.migrations import run_migrations   # si DB ≠ aucune
import logging
import sys
from PyQt6.QtWidgets import QApplication

from views.main_window import MainWindow
from views.main_window import install_excepthook   # défini dans main_window.py

setup_logging()                                    # @rules/logging.md
logger = logging.getLogger(__name__)
logger.info("Démarrage application")

run_migrations()                                   # @rules/db.md (si applicable)

app = QApplication(sys.argv)
# install_translator(app)                          # @rules/i18n.md (si i18n activée)

window = MainWindow()
install_excepthook(window)                         # @rules/errors.md
window.show()

sys.exit(app.exec())
```

**1. Instructions d'installation** — inclure après `requirements.txt` :

```
## Installation

# 1. Créer l'environnement virtuel
python -m venv .venv

# 2. Activer (Windows)
.venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python main.py
```

**2. README.md** — générer à la racine du projet :

```markdown
# [NOM_APP] — v[VERSION]

## Objectif
[Description synthétique issue de la Phase 2]

## Fonctionnalités
- [Liste des fonctionnalités retenues — Phase 2]

## Hors périmètre
- [Liste — Phase 2]

## Stack technique
- OS : Windows
- Framework : PyQt6
- Python : 3.10+
- Icônes : qtawesome
- DB : [valeur]
- i18n : [Oui/Non]
- Tests : [Oui/Non — pytest + pytest-qt si Oui]

## Architecture
[Arborescence du contrat — Phase 4 avec rôle de chaque fichier]

## Installation
[Reprendre les instructions ci-dessus]

## Tests
[Section incluse uniquement si tests activés en Phase 1]

pip install -r requirements-dev.txt
pytest

## Couleur primaire
[Nom + hex clair + hex sombre]
```

---

## Vérification d'intégrité (silencieuse — signalée si écart)

**Chaque lot :**
1. Syntaxe Python valide.
2. Imports : tous utilisés, aucun manquant, séparation MVC respectée.
3. Responsabilités MVC respectées.
4. Zéro `# TODO`, zéro `pass` injustifié.
5. Python 3.10+ · PyQt6 stable · zéro API PyQt5.
6. Conformité `design-system.md` et `layout.md`.

**Dernier lot uniquement — cross-fichiers :**
7. Tous imports inter-couches résolus.
8. Signaux/slots cohérents.
9. Contrat architectural respecté.
10. Zéro valeur visuelle en dur dans Python.
11. README.md généré et complet.

**Lot tests uniquement (si activé) :**
12. Chaque module source a son fichier test correspondant (voir mapping Phase 4).
13. `pytest` exit code 0 — tous les tests passent.

---

## Ajustements post-livraison

Correction isolée sur le fichier concerné + ses dépendances directes.
Réécriture du fichier complet via `Write` (jamais de diff partiel).

## Résolution d'anomalie

Dès que la solution définitive est identifiée et livrée, produire :

```
Anomalie résolue. Éléments à retirer des tentatives précédentes :

Fichier [nom] :
- [ligne / bloc / import / objectName à supprimer]
```