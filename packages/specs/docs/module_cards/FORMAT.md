# Module Card Format (FORMAT v0.1.0)

## Header
- **Module ID**: <short_id>
- **Module Name**: <human-readable name>
- **Version**: <semantic version>
- **Owner**: <team or role>
- **Status**: <alpha|beta|stable|deprecated>
- **Last Updated**: <YYYY-MM-DD>

## Purpose
Briefly state what the module does and why it exists.

## Scope
- **In-scope**: bullets
- **Out-of-scope**: bullets

## Inputs
- **Input Artifacts**: list required inputs and their formats/paths
- **Preconditions**: any required assumptions

## Outputs
- **Output Artifacts**: list outputs and their formats/paths
- **Determinism**: describe deterministic guarantees (e.g., stable hashes)

## Interfaces
- **CLI/API**: primary invocation(s)
- **Config**: supported config flags or files

## Failure Modes
- List common failure modes and where to look (file/function names)

## Verification
- **Canonical Checks**: exact commands to verify

## Notes
- Any caveats or future work
