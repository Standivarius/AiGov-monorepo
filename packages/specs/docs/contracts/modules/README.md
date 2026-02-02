# Module Contracts

This directory contains the module registry, module cards, and the generated dashboard snapshot.

## Module dashboard exporter

Run:

```
python3 tools/export_module_cards_dashboard.py
```

Optional (if executable bit is set):

```
./tools/export_module_cards_dashboard.py
```

This regenerates `packages/specs/docs/contracts/modules/M_Dashboard.md`.
`tools/validate_planning_pack.py` validates that the committed snapshot matches the exporter output.
