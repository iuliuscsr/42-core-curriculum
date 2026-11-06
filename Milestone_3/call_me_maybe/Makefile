.PHONY: install run clean debug lint lint-strict

GOINFRE_DIR := /goinfre/$(USER)/call_me_maybe

export HF_HOME := $(GOINFRE_DIR)/hf_cache
export UV_CACHE_DIR := $(GOINFRE_DIR)/uv_cache
export PYTHONPATH := .
export PYTHONDONTWRITEBYTECODE := 1


install:
	
	@mkdir -p $(GOINFRE_DIR)/venv
	@mkdir -p $(GOINFRE_DIR)/hf_cache
	@mkdir -p $(GOINFRE_DIR)/uv_cache
	
	@if [ ! -L .venv ]; then \
		rm -rf .venv; \
		ln -s $(GOINFRE_DIR)/venv .venv; \
		echo "Symlink to goinfre created."; \
	fi
	@uv sync

run:
	@HF_HUB_OFFLINE=0 TRANSFORMERS_OFFLINE=0 \
	uv run python -m src

debug:
	@uv run python -m pdb -c continue -m src

clean:
	@rm -rf __pycache__ src/__pycache__ .mypy_cache .pytest_cache \
	*.egg-info src/*.egg-info

lint:
	@uv run flake8 src/
	@uv run mypy \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		src/

lint-strict:
	@uv run flake8 src/
	@uv run mypy --strict src/