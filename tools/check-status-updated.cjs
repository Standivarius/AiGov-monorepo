#!/usr/bin/env node
"use strict";

const { execSync } = require("node:child_process");

const run = (cmd) => execSync(cmd, { encoding: "utf8" }).trim();

try {
  execSync("git fetch origin main --depth=1", { stdio: "ignore" });
} catch {
  // Continue with local refs if fetch fails.
}

let changed = [];
try {
  const output = run("git diff --name-only origin/main...HEAD");
  if (output) {
    changed = output.split("\n").filter(Boolean);
  }
} catch (err) {
  console.error("Unable to compute diff against origin/main.");
  console.error(err.message || String(err));
  process.exit(1);
}

if (changed.length === 0) {
  process.exit(0);
}

if (changed.includes("STATUS.md")) {
  process.exit(0);
}

const docsOnly = changed.every((path) => path.startsWith("docs/"));
if (docsOnly) {
  process.exit(0);
}

const important = changed.some((path) => {
  if (path.startsWith("packages/")) return true;
  if (path.startsWith("tools/")) return true;
  if (path.startsWith(".github/workflows/")) return true;
  if (path === "nx.json") return true;
  if (path === "package.json") return true;
  if (path === "package-lock.json") return true;
  if (path.startsWith("devcontainer/")) return true;
  if (path.startsWith(".devcontainer/")) return true;
  return false;
});

if (important) {
  console.error("This PR changes important files but does not update STATUS.md.");
  console.error("Run the Codex skill: status-pr-update to generate a paste-ready snippet, then update STATUS.md.");
  process.exit(1);
}

process.exit(0);
