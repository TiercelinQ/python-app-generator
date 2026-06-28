# Salesforce CLI integration rules — Python/PyQt6 app

> Conditional — only when Phase 1 "Salesforce CLI" = `Yes`. When enabled, the default scaffold is **runner + typed helpers + a starter Org Manager** (`@rules/mvc.md`). Targets the **`sf` v2 CLI** only. The app never handles OAuth tokens — `sf` owns the auth flow and the OS keychain.

The runner is a Model (`models/sf_cli.py`) — strict MVC: the View (Org Manager) emits signals, the Controller calls the runner and intercepts its exceptions, surfacing them via `show_toast` (`@rules/errors.md`).

## Command catalog (source of truth for sf commands/flags)

This rule is the **hub** that routes every sf-aware skill to the command catalog under `.claude/sf-cli-reference/`. Whenever you write or modify an `sf` invocation (a helper's `argv`, a new subcommand, a flag):

1. **Never invent** an `sf` command, subcommand, or flag from memory — verify it against the catalog.
2. Read `sf-cli-reference/INDEX.md` first (small: convention + capability → file map), then **open only the section file** matching the capability you need (`auth-orgs.md`, `metadata-deploy.md`, `apex.md`, `data.md`, `packaging.md`, `users-schema.md`, `platform-api.md`, `advanced.md`). **Never read the whole catalog** — it is large; section-scoped reads keep the context lean.
3. Each catalog entry states the exact flags and whether `--json` / `--api-version` / `-o, --target-org` apply. The typed helpers below source their `argv` from there.
4. The catalog reflects `sf` v2 at a given release; field names/flags drift across versions. For anything uncertain or recent (`advanced.md` plugins), confirm against the installed CLI with `sf <command> --help`.

## Principle

The app shells out to the user's `sf` binary with `--json` and parses the envelope. Everything the integration needs (orgs, auth, SOQL, Tooling API, metadata, Apex) is an `sf` subcommand — no third-party Salesforce Python SDK dependency (no `simple-salesforce`).

- `sf` is a **runtime prerequisite**; if absent → a clear `danger` toast (the runner raises `SfCliNotFoundError`). The official Salesforce tooling is a documented optional recommendation in the README only — never a hard dependency.
- **Resolve `sf` cross-OS via `config.SF_CLI_PATH` + `shutil.which` (no `shell=True`).** Empty `SF_CLI_PATH` → resolve the bare command `sf` from PATH; set → use the configured path. `shutil.which` returns the full resolved path (it honors `PATHEXT` on Windows, so it picks `sf.exe` when present).
- **Windows shim caveat (explicit compromise)** — Python has no `cross-spawn` equivalent. A `sf` installed via `npm i -g @salesforce/cli` is a `sf.cmd` shim, and `subprocess.run([... ], shell=False)` cannot launch a `.cmd`/`.bat` directly (`CreateProcess` raises `OSError [WinError 193]`). The **standalone `sf` installer ships a real `sf.exe`** and avoids this entirely — recommend it in the README. The runner catches the `OSError` and raises `SfCliNotFoundError` with an actionable message rather than branching to `shell=True` (which `@rules/security.md §5` forbids) or `cmd /c`.
- **Install (documented in the README, not imposed)**: the official `sf` installer for the user's OS bundles its own Node; `npm install -g @salesforce/cli` also works (but produces the `.cmd` shim on Windows — see above). The app only needs `sf` reachable (PATH or `SF_CLI_PATH`).

## Runner — `models/sf_cli.py`

```python
"""Salesforce CLI runner — subprocess wrapper with typed helpers."""

import json
import logging
import shutil
import subprocess
from typing import Any

import config
from models.exceptions import SfCliNotFoundError, SfCommandError

logger = logging.getLogger(__name__)


class SfCli:
    """Wraps the `sf` v2 CLI. Resolves the binary cross-OS, runs `sf <args> --json`,
    parses the envelope defensively. Never stores or logs a token — `sf` owns auth."""

    def __init__(self, sf_path: str | None = None) -> None:
        # Empty → resolve `sf` from PATH; set → use the configured path.
        self._configured = sf_path if sf_path is not None else config.SF_CLI_PATH

    def _resolve_bin(self) -> str:
        resolved = shutil.which(self._configured or "sf")
        if resolved is None:
            raise SfCliNotFoundError(
                "Salesforce CLI (sf) introuvable. Installez le CLI (installeur "
                "standalone recommandé : fournit sf.exe) ou renseignez SF_CLI_PATH."
            )
        return resolved

    def run(self, args: list[str]) -> Any:
        """Run `sf <args> --json`. args is a LIST — never a shell string (security)."""
        cmd = [self._resolve_bin(), *args, "--json"]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=config.SF_CLI_TIMEOUT,
                shell=False,  # NON-NEGOTIABLE — @rules/security.md §5
            )
        except OSError as e:  # FileNotFoundError, WinError 193 (.cmd shim not launchable)
            raise SfCliNotFoundError(
                "Salesforce CLI (sf) introuvable ou non exécutable. Sur Windows, "
                "préférez l'installeur standalone (sf.exe) : un shim sf.cmd issu de "
                "`npm i -g` n'est pas lançable directement."
            ) from e
        except subprocess.TimeoutExpired as e:
            raise SfCommandError("Commande sf expirée.") from e

        try:
            parsed = json.loads(proc.stdout or proc.stderr)
        except (json.JSONDecodeError, ValueError) as e:
            raise SfCommandError("Réponse sf illisible.") from e

        if parsed.get("status") != 0:
            raise SfCommandError(parsed.get("message") or "Commande sf en échec.")
        return parsed.get("result")
```

- `subprocess.run([bin, *args, "--json"], shell=False)` — argument list, no shell. User values (alias, SOQL) are **separate list elements**, never spliced into a string. This is the command-injection guard (`@rules/security.md §5`).
- The runner **raises named exceptions** (not a `Result` object) — the idiomatic Python/MVC pattern: the controller catches `SfCliNotFoundError` / `SfCommandError` and calls `view.show_toast("danger", ...)` (`@rules/errors.md`). Uncaught ones reach `sys.excepthook` → danger toast.
- Parse **defensively**: `sf` field names vary across CLI versions. Read the `status`/`result` envelope, guard missing fields with `.get(...)`, and verify the actual shape at generation time against the installed `sf`.
- Never log `proc.stdout`/`stderr` raw if a command can echo a secret — log the summary, not the payload (`@rules/logging.md`).

## Typed helpers (on top of the runner)

```python
list_orgs(self) -> list[OrgInfo]                       # sf org list           → result.nonScratchOrgs / scratchOrgs (defensive)
get_default_org(self) -> str | None                    # sf config get target-org
set_default_org(self, alias: str) -> None              # sf config set target-org=<alias>
login_web(self, alias: str) -> None                    # sf org login web --alias <alias>   (sf opens the browser)
logout(self, alias: str) -> None                       # sf org logout --target-org <alias> --no-prompt
reconnect(self, alias: str) -> None                    # re-run login web for an expired token
query(self, soql: str, org: str | None = None) -> dict # sf data query --query <soql>
query_tooling(self, soql, org=None) -> dict            # sf data query --use-tooling-api --query <soql>
retrieve(self, args) -> dict                           # sf project retrieve start
deploy(self, args) -> dict                             # sf project deploy start
run_apex(self, file: str, org=None) -> dict            # sf apex run --file <file>
```

- Each helper builds the args list and delegates to `run()`. A light `@dataclass OrgInfo` (`alias`, `username`, `connected_status`, `is_default`, `instance_url`) models only the fields the UI uses; build it defensively from the parsed dicts.
- **Every helper's command and flags are verified against the catalog**: orgs/auth/config → `sf-cli-reference/auth-orgs.md`, `query`/`query_tooling` → `data.md`, `run_apex` → `apex.md`, `retrieve`/`deploy` → `metadata-deploy.md`. Do not guess a flag — look it up in the matching section file.

## Auth orchestration

- The app **drives** `sf org login/logout` and `sf config set target-org`; it never reads, writes, or stores a token. `sf` performs the OAuth web flow and stores tokens in its own keychain.
- "Reconnect on expired token" = re-run `sf org login web` for that alias (`connected_status == "RefreshTokenAuthError"`).
- The app may persist a **non-secret** alias in `preferences.json`; never a token. If a real secret ever has to be stored, use `keyring` (`@rules/security.md §3`) — never plain text.

## Starter Org Manager (default scaffold)

One entity = `model + view + controller` (`@rules/mvc.md`). The Org Manager is that entity for the `sf` integration:

- **Model** (`models/sf_cli.py`): the runner + typed helpers above.
- **View** (`views/org_manager_view.py`): a `QTreeView`/`QTreeWidget` listing orgs from `list_orgs()`, connected vs disconnected state and the default org marked, with buttons add / remove / reconnect / set-default / refresh. PyQt6 only, no business logic; `objectName` set, styling via QSS. **State icons use `config.ICON_COLORS`** (`success` for connected, `danger` for expired/disconnected) — the one documented QSS exception (qtawesome).
- **Controller** (`controllers/org_manager_controller.py`): connects the view's signals to the runner helpers, validates input (alias non-empty) before calling, `try/except` around each call → `view.show_toast(...)`, and refreshes the list after any mutating action. A destructive action (remove/logout) is confirmed in the view before the controller runs it.

## Anti-patterns — what NOT to do

- **Do not** build the `sf` command as a string or use `subprocess`/`QProcess` with `shell=True` and interpolated input — pass an args list, `shell=False`.
- **Do not** call `sf` outside `models/sf_cli.py` (no `subprocess` in a view/controller) or invent a command/flag not in `sf-cli-reference/`.
- **Do not** read, store, or log an org token — `sf` owns tokens; the app stores at most a non-secret alias.
- **Do not** add a third-party Salesforce SDK (`simple-salesforce`…) for the v1 use cases — the CLI covers them.
- **Do not** return a raw exception from a controller to a view — intercept it and `show_toast` (`@rules/errors.md`).
- **Do not** branch to `shell=True` or `cmd /c` to launch a `.cmd` shim — recommend the standalone `sf.exe` and raise a clear `SfCliNotFoundError`.
- **Do not** assume exact `sf --json` field names — parse defensively (`.get`) and verify against the installed CLI.
- **Do not** target `sfdx` (legacy) — `sf` v2 only.

## Integrity verification

Detailed in `@rules/verification.md`. Key points (if sf enabled): all `sf` calls go through `models/sf_cli.py` via `subprocess.run` with an args list (no `shell=True`, no view/controller spawn); `sf` resolved from PATH or `config.SF_CLI_PATH` via `shutil.which`; not found / not launchable → `SfCliNotFoundError` → danger toast; no token stored/logged; `SfCliNotFoundError` + `SfCommandError` defined in `models/exceptions.py`; Org Manager controller validates input + refreshes the view; README documents the cross-OS `sf` prerequisite (standalone installer recommended) + `SF_CLI_PATH`.
