#!/usr/bin/env node
"use strict";

const { execSync } = require("node:child_process");
const fs = require("node:fs");

const run = (cmd) => execSync(cmd, { encoding: "utf8" }).trim();

try {
  // Best effort: make sure origin/main exists (CI should also use fetch-depth: 0).
  execSync("git fetch origin main --depth=1", { stdio: "ignore" });
} catch {
  // Continue with local refs if fetch fails.
}

let changed = [];
try {
  const output = run("git diff --name-only origin/main...HEAD");
  changed = output.split("\n").map((s) => s.trim()).filter(Boolean);
} catch (err) {
  console.error("Unable to compute diff against origin/main.");
  console.error(err?.message || String(err));
  process.exit(1);
}

if (changed.length === 0) {
  process.exit(0);
}

const statusChanged = changed.includes("STATUS.md");

// If STATUS.md was changed, validate it so conflict junk can't slip through.
if (statusChanged) {
  let statusText = "";
  try {
    statusText = fs.readFileSync("STATUS.md", "utf8");
  } catch (err) {
    console.error("STATUS.md was changed but could not be read.");
    console.error(err?.message || String(err));
    process.exit(1);
  }

  const conflictMarkers = ["<<<<<<<", "=======", ">>>>>>>"];
  const hasConflictMarkers = conflictMarkers.some((m) => statusText.includes(m));
  if (hasConflictMarkers) {
    console.error("STATUS.md contains merge-conflict markers (<<<<<<< / ======= / >>>>>>>).");
    console.error("Resolve the conflict cleanly before merging.");
    process.exit(1);
  }

  // Catch the common GitHub conflict-editor leak: bare branch names ending up as lines in STATUS.md.
  const lines = statusText.split(/\r?\n/).map((l) => l.trim());
  const badBranchLines = lines.filter(
    (l) => l === "main" || l === "master" || /^chore\/[A-Za-z0-9._-]+$/.test(l)
  );
  if (badBranchLines.length > 0) {
    console.error("STATUS.md contains bare branch-name lines that usually come from conflict resolution:");
    console.error("  " + badBranchLines.slice(0, 10).join(", "));
    console.error("Remove these lines and keep only real STATUS entries.");
    process.exit(1);
  }

  // Enforce a single canonical "Next:" line to avoid repeated/contradicting Next pointers.
  const nextLines = statusText.match(/^\s*-\s*Next:/gm) || [];
  if (nextLines.length > 1) {
    console.error(`STATUS.md contains ${nextLines.length} "- Next:" lines.`);
    console.error('Keep exactly one canonical "- Next:" line to prevent confusion and future conflicts.');
    process.exit(1);
  }

  // If STATUS.md was updated and is clean, we're good regardless of other changes.
  process.exit(0);
}

// Exception: docs-only PRs do not require STATUS.md updates.
const nonDocsChanges = changed.filter((p) => !p.startsWith("docs/"));
if (nonDocsChanges.length === 0) {
  process.exit(0);
}

// Require STATUS.md update when "important areas" are touched.
const important = changed
  .filter((p) => p !== "STATUS.md")
  .some((path) => {
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
  console.error(
    "Run the Codex skill: status-pr-update to generate a paste-ready snippet, then update STATUS.md."
  );
  process.exit(1);
}

process.exit(0);
