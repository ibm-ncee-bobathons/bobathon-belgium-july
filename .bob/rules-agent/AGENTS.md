# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Coding Rules (Non-Obvious)

- **Never run commands from repo root** — each lab is independent; `cd` into the specific lab dir first.
- Lab 1 test file (`test_app.py`) lives alongside source, not in a `tests/` subdirectory — this is intentional.
- Lab 5 tests **must** go in `tests/` at the project root (enforced by `.bob/rules-test-engineer/testing-rules.md`).
- Always use `python -m pytest`, never bare `pytest` — avoids path resolution issues.
- `# Made with Bob` footer comment is expected on generated files in Lab 1.
- Lab 5 error boundary: internal helpers raise `ValueError`; only the FastAPI route handlers convert to `HTTPException` — do not raise `HTTPException` from helper functions.
- watsonx Orchestrate ADK deployment uses `import-all.sh` CLI script, not Python — do not substitute with SDK calls.
- When adding a new custom mode, the rules directory must be named `rules-{slug}` matching the mode's `slug` field exactly.
