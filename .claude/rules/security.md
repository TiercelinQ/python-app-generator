# Security rules — Python/PyQt6

Applied to 100% of generated applications. Any deviation requires the contract declaration protocol (stop → declare → validate).

## 1. Input validation

- Every value entering a model (from a view, a file, an import) is validated before use: type, mandatory fields, bounds, format.
- Validation lives in `models/` (business rules) or `utils/helpers.py` (pure format checks: email, numeric, date). Views may pre-validate for UX but the model is the authority.
- Raise a named `ValidationError` (`models/exceptions.py`) on invalid data — never silently coerce.

## 2. SQL — always parameterized

- 100% parameterized queries (`?` placeholders + params tuple). Zero string concatenation / f-string interpolation of values into SQL. Detail and access pattern: `@rules/db.md`.
- All DB access through `models/db.py` — no `sqlite3.connect` / `psycopg.connect` elsewhere.

## 3. Secrets

- No hardcoded secret (API key, token, password) in the code, `config.py`, or `preferences.json`.
- User secrets, when required: OS-backed store via `keyring` (validate the dependency in Phase 1). Never plain text on disk.
- Never log a secret, token, or personally identifiable value (`@rules/logging.md`).

## 4. File system

- Paths received from the user (file dialogs, drag-drop, import) are resolved (`Path(...).resolve()`) and checked to stay under an allowed directory before read/write — zero path traversal.
- Application data (DB, `preferences.json`, logs) lives in the project root in dev and `%APPDATA%/[AppName]/` when packaged — never in arbitrary user locations.

## 5. Process / code execution

- No `eval`, `exec`, or `pickle.load` on untrusted input.
- Subprocesses: `subprocess.run([...], shell=False)` with an argument list — never `shell=True` with an interpolated string. Same rule for `QProcess` (pass program + args separately).
- No dynamic import of a module name coming from user input.

## 6. Dependencies

- Only libraries validated in Phase 1. Pin minimum versions (`@rules/config.md`).
- No remote code download at runtime; everything ships via `requirements.txt`.

## Anti-patterns — what NOT to do

- **Do not** build a SQL string by concatenation/f-string with a value — parameterize.
- **Do not** hardcode a secret or store it in plain text — use `keyring`.
- **Do not** open/write a user-supplied path without resolving and bounding it.
- **Do not** call `subprocess`/`QProcess` with `shell=True` or an interpolated command string.
- **Do not** use `eval`/`exec`/`pickle` on untrusted data.
- **Do not** log secrets or PII.

## Integrity verification

Detailed in `@rules/verification.md`. Key points: no hardcoded secret in source/config; all SQL parameterized; user paths resolved + bounded; no `shell=True` / `eval` / `exec` on untrusted input; secrets (if any) via `keyring`.
