# Makefile for LexiLocal development

.PHONY: help install install-dev test lint format type-check clean run run-test docker-build docker-run

# Default target
help:
	@echo "LexiLocal Development Commands:"
	@echo "  install      Install package and dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  test         Run unit tests"
	@echo "  lint         Run code linting"
	@echo "  format       Format code with black and isort"
	@echo "  type-check   Run type checking with mypy"
	@echo "  clean        Clean build artifacts"
	@echo "  run          Run the Streamlit application"
	@echo "  run-test     Run performance tests"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run Docker container"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Testing
test:
	python -m pytest tests/ -v

test-coverage:
	python -m pytest tests/ --cov=src/lexilocal --cov-report=html --cov-report=term

# Code quality
lint:
	flake8 src/ tests/ scripts/
	black --check src/ tests/ scripts/
	isort --check-only src/ tests/ scripts/

format:
	black src/ tests/ scripts/
	isort src/ tests/ scripts/

type-check:
	mypy src/lexilocal/

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Running
run:
	streamlit run app.py

run-test:
	python scripts/run_performance_test.py

# Docker
docker-build:
	docker build -t lexilocal .

docker-run:
	docker run -p 8501:8501 lexilocal

# Development workflow
dev-setup: install-dev
	@echo "Development environment setup complete!"

check: lint type-check test
	@echo "All checks passed!"

# Release
build:
	python -m build

upload-test:
	python -m twine upload --repository testpypi dist/*

upload:
	python -m twine upload dist/*