# Dev Container Persistence

## What changed and why
- Extensions are pinned in `devcontainer.json` so they auto-install on rebuild.
- GitHub CLI is installed via a Dev Container Feature (no manual install).
- Two Docker volumes persist minimal state:
  - `/home/vscode/.vscode-server` for VS Code server + extension state (includes OpenAI/Codex login).
  - `/home/vscode/.config/gh` for GitHub CLI auth.

## Manage extensions/tools
- Add/remove extensions under `customizations.vscode.extensions` in `.devcontainer/devcontainer.json`.
- Add/remove tools via `features` in `.devcontainer/devcontainer.json`.

## Reset persisted state
- VS Code server state: remove the Docker volume `aigov-vscode-server`.
- GitHub CLI auth state: remove the Docker volume `aigov-gh-config`.

## Token storage note
- GitHub tokens live under `/home/vscode/.config/gh`.
- OpenAI/Codex extension state is stored under `/home/vscode/.vscode-server`.
