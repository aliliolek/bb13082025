.PHONY: run test format lint

run:
python -m src.app.main

test:
pytest -q

format:
black .

lint:
ruff check .
