// Role: static integrity checks of verification.md section B by pattern search, instead of model reading.
// Inputs: <root> (root of the generated PySide6 app)
// Outputs: stdout = one "[point] file:line: message" line per finding, then a total; "OK" if none.
//   Points: 4 TODO · 6 literal hex colors outside config.py, inline setStyleSheet literals · 7 QMessageBox ·
//   8 shell=True/eval/exec, concatenated SQL · logging print( · db connect outside models/db.py ·
//   13 versions (config.py vs changelog) · 14 .gitignore.
// Exit codes: 0 no finding, 1 at least one finding, 4 invalid argument.
// Documented exceptions (ICON_COLORS, SPLASH_COLORS, NATIVE_PALETTE in config.py) are excluded by file;
//   other tolerated cases stay to be judged by the model.
// Command replaced: /python-p5-development, /python-add-feature, /python-fix-issue, section B.
// Example: node .claude/scripts/static-checks.mjs C:\projects\MyApp

import { readdirSync, readFileSync, existsSync, statSync } from "node:fs";
import { join, relative } from "node:path";

const root = process.argv[2];
if (!root || !existsSync(root)) {
  console.error("Usage: static-checks.mjs <root>");
  process.exit(4);
}

const findings = [];
const add = (point, file, line, msg) => findings.push(`[${point}] ${file}${line ? ":" + line : ""}: ${msg}`);
const rel = (f) => relative(root, f).split("\\").join("/");

function walk(dir, out = []) {
  if (!existsSync(dir)) return out;
  for (const e of readdirSync(dir)) {
    if ([".venv", "venv", "__pycache__", ".git", "node_modules", "dist", "build"].includes(e)) continue;
    const p = join(dir, e);
    statSync(p).isDirectory() ? walk(p, out) : out.push(p);
  }
  return out;
}

const py = walk(root).filter((f) => f.endsWith(".py") && !rel(f).startsWith("tests/") && !rel(f).startsWith("scripts/"));
const notConfig = (f) => rel(f) !== "config.py";
const rules = [
  { point: "4", re: /#\s*TODO/, msg: "# TODO is forbidden" },
  { point: "6", re: /["']#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?["']/, msg: "literal hex color outside config.py", only: notConfig },
  { point: "6", re: /setStyleSheet\(\s*f?["']/, msg: "inline setStyleSheet literal, route it through the QSS sheets" },
  { point: "7", re: /\bQMessageBox\b/, msg: "QMessageBox is forbidden for a business error" },
  { point: "8", re: /shell\s*=\s*True/, msg: "shell=True is forbidden" },
  { point: "8", re: /\b(eval|exec)\s*\(/, msg: "eval/exec is forbidden on untrusted input" },
  { point: "8", re: /\.execute(many)?\(\s*(f["']|["'][^"']*["']\s*(\+|%)|[^,)]*\.format\()/, msg: "concatenated or formatted SQL, use ? parameters" },
  { point: "logging", re: /\bprint\s*\(/, msg: "print( is forbidden, use the logger" },
  { point: "db", re: /\b(sqlite3|psycopg2?|pg8000)\.connect\(/, msg: "database connect outside models/db.py", only: (f) => rel(f) !== "models/db.py" },
];
for (const f of py) {
  const lines = readFileSync(f, "utf8").split(/\r?\n/);
  for (const r of rules) {
    if (r.only && !r.only(f)) continue;
    lines.forEach((l, i) => {
      if (r.re.test(l)) add(r.point, rel(f), i + 1, r.msg);
    });
  }
}

// Point 13: config.py APP_VERSION must equal the top released changelog version
const ver = {};
try {
  ver["config.py APP_VERSION"] = readFileSync(join(root, "config.py"), "utf8").match(/APP_VERSION\s*(?::\s*\w+)?\s*=\s*["']([^"']+)/)?.[1];
  ver["CHANGELOG top"] = readFileSync(join(root, "docs/release/CHANGELOG.md"), "utf8").match(/^## \[(\d+\.\d+\.\d+)\]/m)?.[1];
} catch {
  add("13", "docs/release/CHANGELOG.md", 0, "config.py or changelog is unreadable");
}
if (Object.values(ver).some((v) => v === undefined) || new Set(Object.values(ver)).size > 1)
  add("13", "(versions)", 0, `versions differ or are missing: ${JSON.stringify(ver)}`);

// Point 14: .gitignore
const gi = join(root, ".gitignore");
if (!existsSync(gi)) add("14", ".gitignore", 0, "file is missing");
else {
  const set = new Set(readFileSync(gi, "utf8").split(/\r?\n/).map((l) => l.trim()));
  for (const need of ["__pycache__/", "*.py[cod]", ".venv/", "venv/", "/dist/", "/build/", "*.egg-info/", ".env", "/data/", "/logs/", "/preferences.json", "tasks/", ".claude/settings.local.json", ".claude/agent-memory/"])
    if (!set.has(need)) add("14", ".gitignore", 0, `missing entry: ${need}`);
  for (const bad of ["build.spec", "tests/", ".claude/settings.json", "docs/release/CHANGELOG.md", "CLAUDE.md"])
    if (set.has(bad)) add("14", ".gitignore", 0, `must not ignore: ${bad}`);
}

console.log(findings.length ? `${findings.join("\n")}\n\n${findings.length} finding(s).` : "OK: no finding.");
process.exit(findings.length ? 1 : 0);
