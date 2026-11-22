// Role: run the executable verification ladder (verification.md section A) and summarize the result.
// Inputs: <root> [--venv <dir>]
//   Interpreter: <venv>/Scripts/python.exe (or bin/python), defaulting to <root>/.venv when it exists, else "python".
//   Commands: python -m ruff check ., python -m ruff format --check ., python -m mypy .,
//   python -m pytest (only if tests/ exists). Stops at the first failing command.
// Outputs: stdout = command / status / duration table, then the first diagnostic lines of the failure.
// Exit codes: 0 all green, 1 a command failed, 4 invalid argument.
// Not covered: the smoke launch "python main.py", which stays manual (confirm a window opens, no startup crash).
// Command replaced: /python-run-tests, step 1 (interpreting a failure stays with the model).
// Example: node .claude/scripts/run-verification.mjs C:\projects\MyApp --venv C:\projects\MyApp\.venv

import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { join } from "node:path";

const args = process.argv.slice(2);
const vi = args.indexOf("--venv");
const venvArg = vi >= 0 ? args.splice(vi, 2)[1] : "";
const root = args[0];
if (!root || !existsSync(root) || (vi >= 0 && !venvArg)) {
  console.error("Usage: run-verification.mjs <root> [--venv <dir>]");
  process.exit(4);
}

const venv = venvArg || (existsSync(join(root, ".venv")) ? join(root, ".venv") : "");
let python = "python";
if (venv) {
  const candidates = [join(venv, "Scripts", "python.exe"), join(venv, "bin", "python")];
  python = candidates.find((c) => existsSync(c)) ?? "";
  if (!python) {
    console.error(`No interpreter found in ${venv}.`);
    process.exit(4);
  }
}

const steps = [
  { label: "ruff check .", argv: ["-m", "ruff", "check", "."] },
  { label: "ruff format --check .", argv: ["-m", "ruff", "format", "--check", "."] },
  { label: "mypy .", argv: ["-m", "mypy", "."] },
];
if (existsSync(join(root, "tests"))) steps.push({ label: "pytest", argv: ["-m", "pytest"] });

const rows = [];
let failure = null;
for (const s of steps) {
  if (failure) {
    rows.push([s.label, "not run", "-"]);
    continue;
  }
  const t0 = Date.now();
  const r = spawnSync(python, s.argv, { cwd: root, encoding: "utf8", timeout: 10 * 60 * 1000, maxBuffer: 64 * 1024 * 1024 });
  const secs = ((Date.now() - t0) / 1000).toFixed(1) + " s";
  if (r.error) {
    rows.push([s.label, `FAILED (${r.error.message})`, secs]);
    failure = { label: s.label, output: String(r.error.message) };
  } else if (r.status === 0) rows.push([s.label, "OK", secs]);
  else {
    rows.push([s.label, `FAILED (code ${r.status ?? r.signal ?? "?"})`, secs]);
    failure = { label: s.label, output: `${r.stdout ?? ""}\n${r.stderr ?? ""}`.trim() };
  }
}

console.log("| Command | Status | Duration |\n|---|---|---|");
for (const r of rows) console.log(`| ${r.join(" | ")} |`);
if (failure) {
  const diag = failure.output.split(/\r?\n/).filter((l) => /error|would reformat|FAILED|\b[A-Z]{1,3}\d{3,4}\b/.test(l)).slice(0, 15);
  console.log(`\nFirst diagnostics from "${failure.label}":`);
  console.log((diag.length ? diag : failure.output.split(/\r?\n/).slice(-15)).join("\n"));
  process.exit(1);
}
