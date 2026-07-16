.PHONY: clean format lint test train help

VENV := venv
PYTHON := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip

help:
	@echo "Available commands:"
	@echo "  make setup    : Set up virtual environment and install dependencies"
	@echo "  make clean    : Remove build artifacts and cache directories"
	@echo "  make format   : Run black and isort"
	@echo "  make lint     : Run flake8 and mypy"
	@echo "  make test     : Run tests using pytest"
	@echo "  make train    : Run the training script (dummy for now)"

setup:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(VENV)/Scripts/pre-commit install

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

format:
	$(VENV)/Scripts/black src tests scripts
	$(VENV)/Scripts/isort src tests scripts

lint:
	$(VENV)/Scripts/flake8 src tests scripts
	$(VENV)/Scripts/mypy src tests scripts

test:
	$(VENV)/Scripts/pytest tests/

train:
	$(PYTHON) scripts/train.py
