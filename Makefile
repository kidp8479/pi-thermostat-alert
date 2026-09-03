.PHONY: install format format-check lint lint-check test check

VENV := .venv
PY := $(VENV)/bin/python

# Create the venv, install the project with dev extras, enable the hook.
install:
	python3 -m venv $(VENV)
	$(PY) -m pip install -q -e ".[dev]"
	git config core.hooksPath .githooks
	@echo "done - pre-commit hook enabled"

format:
	$(PY) -m ruff format .

format-check:
	$(PY) -m ruff format --check .

lint:
	$(PY) -m ruff check --fix .

lint-check:
	$(PY) -m ruff check .

test:
	$(PY) -m pytest -q

# Everything CI runs.
check: format-check lint-check test
