# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Repository Purpose

This is a **workshop/lab content repository** for IBM Bobathon Belgium. It contains instructional materials, not a single deployable application. Each lab is self-contained in its own directory.

## Lab Stack Summary

| Lab | Stack | Runtime |
|-----|-------|---------|
| Lab 1 | Python Flask + SQLAlchemy + SQLite / Vanilla JS | Python 3.8+ |
| Lab 2 | Python + watsonx Orchestrate ADK (`ibm-watsonx-orchestrate==2.9.0`) | Python 3.11+ |
| Lab 3 | Python + `confluent-kafka` + `fastmcp` + `ibm-watsonx-orchestrate==2.9.0` | Python 3.11+ |
| Lab 5 | Python FastAPI + pydantic + pytest | Python 3.8+ |
| Optional COBOL | COBOL source files → Java 11+/Maven migration target | Java 11+ |

## Commands

**All commands must be run from the specific lab subdirectory, not the repo root.**

### Lab 1 (Flask backend)
```bash
cd "Lab 1 - Building a Todo Application with Bob/starter/backend"
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py                                              # runs on port 5000
python -m pytest test_app.py -v                           # run all tests
python -m pytest test_app.py::TodoAPITestCase::test_get_todos_empty -v  # single test
bash run_tests.sh                                         # tests + HTML coverage
```

### Lab 5 (FastAPI converter)
```bash
cd "Lab 5 - Custom Modes - Test Engineer Mode Demonstration"
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/converter.py                                   # runs on port 8000
python -m pytest tests/ -v                                # run all tests
python -m pytest tests/test_ping.py -v                    # single test file
python -m pytest tests/test_ping.py::test_name -v         # single test
python -m pytest tests/ --cov=src --cov-report=term-missing -v  # with coverage
```

**Always use `python -m pytest`, never bare `pytest`.**

## Critical Patterns

### Custom Modes (Lab 5 teaches this)
- Custom mode YAML lives in `.bob/custom_modes.yaml` at the project root
- Mode-specific rules go in `.bob/rules-{slug}/` (e.g., `.bob/rules-test-engineer/`)
- Slash commands go in `.bob/commands/*.md` with YAML frontmatter (`description:` field)
- `fileRegex` in mode `groups.edit` restricts which files the mode can write

### watsonx Orchestrate ADK (Lab 2 & 3)
- Copy `.env.example` → `.env` before starting (each lab has its own)
- ADK project structure: `tools/` for flows/Python tools, `agents/` for YAML configs, `import-all.sh` for deployment
- Use `@flow` decorator for flows, `@tool` decorator for Python tools
- Reference `wxo-implementation-guide.md` in Lab 2 before implementing

### Lab 3 Kafka
- Requires Confluent Cloud credentials in `.env` (bootstrap servers, API key/secret, ksqlDB endpoint)
- Agent YAML configs are in `assets/` not generated at runtime

## Testing Conventions (Lab 1 vs Lab 5)

- **Lab 1**: Uses `unittest.TestCase` with Flask test client; tests in `test_app.py` alongside source
- **Lab 5**: Uses `pytest` with `httpx` TestClient; tests **must** be in `tests/` directory at project root (not inside `src/`)
- Test file naming: `test_*.py` convention enforced in Lab 5 rules

## Code Style (Python)

- Type hints used in Lab 5 FastAPI code (`dict[str, str]`, `Any`, Pydantic `BaseModel`)
- Docstrings on all Flask routes in Lab 1 (Args/Returns format)
- `# Made with Bob` comment at end of generated files (Lab 1 pattern)
- Lab 5 API errors raise `HTTPException` with explicit `status_code` and `detail`; internal helpers raise `ValueError` which callers convert to `HTTPException`
