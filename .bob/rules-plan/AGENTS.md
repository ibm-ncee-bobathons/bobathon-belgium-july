# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Architecture Constraints (Non-Obvious)

- **This repo has no shared code** — each lab is fully isolated with its own `requirements.txt` and `.env`. Do not propose cross-lab shared utilities.
- Lab 2 and Lab 3 both pin `ibm-watsonx-orchestrate==2.9.0` — any new Lab 2/3 work must remain compatible with this version.
- Lab 5 FastAPI app is designed with a deliberate split: pure Python conversion helpers (`yaml_to_python`, `json_to_python`, etc.) are kept separate from FastAPI route handlers to allow unit testing without an HTTP layer.
- Custom modes use `fileRegex` in the `groups.edit` section to enforce file-access restrictions — this is a security/safety guardrail, not just a style choice.
- Bob rule directories follow a strict naming convention: `.bob/rules-{mode-slug}/` — deviation silently breaks rule loading.
- New labs should follow the pattern: lab dir → `README.md` + `requirements.txt` + `.env.example` + source + `assets/` or `images/`.
