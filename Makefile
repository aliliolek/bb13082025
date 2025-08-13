.PHONY: run test format lint

run:
	python -m src.app.main

test:
	python -m pytest -q

format:
	python -m black .

lint:
	python -m ruff check .
