# Based Labs Content Pipeline Makefile

.PHONY: help install dev test clean docker-up docker-down migrate

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies
	pip install -r requirements.txt

dev: ## Start development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
	pytest tests/ -v

clean: ## Clean up cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

docker-up: ## Start all services with Docker Compose
	docker-compose up -d

docker-down: ## Stop all Docker services
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

migrate: ## Run database migrations
	alembic upgrade head

create-migration: ## Create new migration (usage: make create-migration MESSAGE="description")
	alembic revision --autogenerate -m "$(MESSAGE)"

worker: ## Start Celery worker
	celery -A app.worker worker --loglevel=info

scheduler: ## Start Celery beat scheduler
	celery -A app.worker beat --loglevel=info

frontend-install: ## Install frontend dependencies
	cd frontend && npm install

frontend-dev: ## Start frontend development server
	cd frontend && npm start

frontend-build: ## Build frontend for production
	cd frontend && npm run build

lint: ## Run code linting
	black app/ tests/
	flake8 app/ tests/

type-check: ## Run type checking
	mypy app/

setup-dev: install migrate ## Set up development environment
	@echo "Development environment ready!"
	@echo "Run 'make dev' to start the API server"
	@echo "Run 'make frontend-dev' to start the frontend"