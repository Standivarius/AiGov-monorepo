const { spawnSync } = require("node:child_process");

function run(cmd, args) {
  const res = spawnSync(cmd, args, { stdio: "inherit" });
  if (res.error) throw res.error;
  process.exit(res.status ?? 1);
}

if (process.platform === "win32") {
  run("powershell", ["-ExecutionPolicy", "Bypass", "-File", ".\\tools\\run-evalset-migration-smoke.ps1"]);
} else {
  run("bash", ["./tools/run-evalset-migration-smoke.sh"]);
}
