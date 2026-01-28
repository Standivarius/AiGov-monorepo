# GDPR Base Scenario Library Status Report

Run the report:

```bash
python3 tools/report_gdpr_library_status.py
```

The report summarizes total scenarios, ID ranges (including missing IDs), and counts by role, surface tag, and signal ID.

**SOURCES mismatch** means `SOURCES.md` headings (`## GDPR-###`) do not match the scenario IDs present in the library. The tool exits nonzero when any scenario is missing from `SOURCES.md` or when `SOURCES.md` references a scenario that does not exist.
