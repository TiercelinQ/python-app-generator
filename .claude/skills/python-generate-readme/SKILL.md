---
name: python-generate-readme
description: Analyze the specs and source of an existing Python/PyQt6 project and generate its README.md (objective, features, stack, tree, conventions, installation). Invoke from the target project root.
model: sonnet
---

# /python-generate-readme — Generate the README.md

## Role
Technical writer — produce an accurate project README from specs + code.

## Goal
Write a README that reflects what was actually built.

## Deliverable
`README.md` at the project root.

---

Use the native Claude Code tools (no shell — Windows-compatible):

1. **Sources, in priority**: `docs/specs/*` (especially `04-architect.md`) for the intended structure, then the real code:
   - List Python files via `Glob` `**/*.py` (exclude `__pycache__/`, `.venv/`, `venv/`).
   - Read `config.py`, `requirements.txt`, `main.py` (ignore if absent).
   - Detect `tests/` via `Glob` `tests/**/*.py`; read `requirements-dev.txt` if present.
   - When specs and code disagree, the code is what shipped — describe the code and note the divergence.
2. Generate `README.md` at the root via `Write`:

```markdown
# [NOM_APP] — v[VERSION]

## Objective
[Inferred from docs/specs, config.py, main.py and the structure]

## Features
- [Inferred from the present views/ and controllers/]

## Technical stack
- OS: Windows · Framework: PyQt6 · Python: 3.12+ · Icons: qtawesome
- DB: [inferred from config.py or models/]
- i18n: [Yes/No — inferred from resources/i18n/ or config.py]
- Salesforce CLI: [Yes/No — inferred from models/sf_cli.py + SF_CLI_PATH in config.py]
- Tests: [Yes (pytest + pytest-qt) | No — inferred from the presence of tests/]

## Architecture
[Actual file tree with the role of each file]

## Conventions
[MVC, QSS tokens, toasts, security — pointer to the rules]

## Prerequisites
<!-- Only if models/sf_cli.py is present: the `sf` v2 CLI must be installed and on the PATH (or set `SF_CLI_PATH` in config.py). The standalone installer ships a real `sf.exe` and avoids the Windows npm `.cmd` shim limitation. The Salesforce DX tooling is an optional recommendation, not required. -->

## Installation
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py

## Tests
[Section included only if tests/ detected]
pip install -r requirements-dev.txt
pytest

## Palette
[Name or custom; 5 roles (main background, secondary background, accent, text, details) inferred from the QSS sheets + PRIMARY_* / ICON_COLORS in config.py — otherwise default "Steel Blue" palette]
```

3. Write the file via `Write` (never `cat`/heredoc — Windows-incompatible).
4. If anything is undeterminable from specs + code: ask the closed questions with `AskUserQuestion` (clickable options) before writing.

Confirm with: `README.md generated at the project root.`
