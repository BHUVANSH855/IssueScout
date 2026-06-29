# Contributing to IssueScout

Thank you for your interest in contributing to IssueScout! 🚀

We welcome bug reports, feature requests, documentation improvements, and code contributions.

---

## Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/BHUVANSH855/IssueScout.git
cd IssueScout/backend
```

### 2. Create a virtual environment

Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the project

```bash
pip install -e .
```

### 4. Install development tools

```bash
pip install pytest pytest-cov ruff pre-commit
```

---

## Running Tests

Run the full test suite:

```bash
python -m pytest
```

Run tests with coverage:

```bash
python -m pytest --cov=issuescout --cov-report=term-missing
```

---

## Code Quality

Run Ruff:

```bash
ruff check .
```

Automatically fix issues:

```bash
ruff check . --fix
```

Format code:

```bash
ruff format .
```

---

## Pre-commit

Install hooks:

```bash
pre-commit install
```

Run manually:

```bash
pre-commit run --all-files
```

---

## Branch Naming

Examples:

```
feature/github-pagination
fix/client-timeout
docs/update-readme
test/metadata-similarity
refactor/github-client
```

---

## Commit Messages

Follow Conventional Commits.

Examples:

```
feat: add GitHub pagination helper

fix: handle missing repository metadata

docs: update README

test: improve GitHub client coverage

refactor: simplify scanner pipeline
```

---

## Pull Requests

Before submitting a pull request, ensure:

- All tests pass
- Ruff passes without errors
- New functionality includes tests
- Documentation is updated when necessary

---

## Reporting Issues

When opening an issue, include:

- Operating System
- Python version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Logs or screenshots (if applicable)

---

Thank you for helping improve IssueScout!
