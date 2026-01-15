#!/usr/bin/env node
"use strict";

const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const repoRoot = path.resolve(__dirname, "..");
const scriptPath = path.join(repoRoot, "tools", "run-evalset-migration-smoke.sh");

if (!fs.existsSync(scriptPath)) {
  console.error(`Missing runner: ${scriptPath}`);
  process.exit(1);
}

const result = spawnSync("bash", [scriptPath], { stdio: "inherit" });
if (result.error) {
  if (result.error.code === "ENOENT") {
    console.error("bash not found. Run this target in WSL/Linux with bash available.");
    process.exit(1);
  }
  throw result.error;
}
process.exit(result.status ?? 1);
