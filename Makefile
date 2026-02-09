.PHONY: help install dev-install test lint format clean docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make dev-install  - Install development dependencies"
	@echo "  make test         - Run all tests"
	@echo "  make test-unit    - Run unit tests only"
	@echo "  make test-int     - Run integration tests only"
	@echo "  make lint         - Run all linters"
	@echo "  make format       - Format code with black and isort"
	@echo "  make clean        - Clean up generated files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make run          - Run development server"

install:
	pip install -r requirements/prod.txt

dev-install:
	pip install -r requirements/dev.txt

test:
	pytest tests/ -v --cov=src --cov-report=html

test-unit:
	pytest tests/unit -v

test-int:
	pytest tests/integration -v

lint:
	ruff check src/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".mypy_cache" -delete
	find . -type d -name "htmlcov" -delete
	rm -f .coverage
	rm -rf build/ dist/ *.egg-info/

docker-build:
	docker-compose -f docker/docker-compose.yml build

docker-up:
	docker-compose -f docker/docker-compose.yml up -d

docker-down:
	docker-compose -f docker/docker-compose.yml down

run:
	python -m src.main
