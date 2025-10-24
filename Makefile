.PHONY: install fmt lint typecheck test clean fix-colima

install:
	pip install -e ".[dev]"

fmt:
	ruff format src tests
	ruff check --fix src tests

lint:
	ruff check src tests

typecheck:
	mypy src tests

test:
	pytest tests/ -v

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

fix-colima:
	./fix-colima.sh

