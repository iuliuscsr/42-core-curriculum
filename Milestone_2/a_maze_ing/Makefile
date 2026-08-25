.PHONY: install run debug clean lint

install:
	pip install build
	pip install .

build-pkg:
	python3 -m build

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache *.egg-info dist build

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .