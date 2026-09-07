.PHONY: install run debug clean lint build-pkg

PYTHON = ./env/bin/python3

install:
	test -d env || python3 -m venv env
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install mlx-2.2-py3-none-any.whl
	$(PYTHON) -m pip install -e .

build-pkg:
	$(PYTHON) -m build
	cp dist/mazegen-1.0.0* .
	rm -rf dist

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache *.egg-info dist build src/*.egg-info src/__pycache__

venv-clean: clean
	rm -rf env/

lint:
	$(PYTHON) -m flake8 . --exclude env/
	$(PYTHON) -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .