.PHONY: help build dev prod test clean ssl logs

# Default target
help:
	@echo "IdeaHub - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Start development environment"
	@echo "  make dev-build    - Build and start development environment"
	@echo "  make dev-logs     - Show development logs"
	@echo "  make dev-stop     - Stop development environment"
	@echo ""
	@echo "Production:"
	@echo "  make prod         - Start production environment"
	@echo "  make prod-build   - Build and start production environment"
	@echo "  make prod-logs    - Show production logs"
	@echo "  make prod-stop    - Stop production environment"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo ""
	@echo "Utilities:"
	@echo "  make ssl          - Generate SSL certificates"
	@echo "  make clean        - Clean up containers and volumes"
	@echo "  make logs         - Show all logs"

# Development commands
dev:
	docker-compose -f docker-compose.dev.yml up

dev-build:
	docker-compose -f docker-compose.dev.yml up --build

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

dev-stop:
	docker-compose -f docker-compose.dev.yml down

# UI Development commands
ui-dev:
	cd ui && npm run dev

ui-build:
	cd ui && npm run build

ui-install:
	cd ui && npm install

ui-test:
	cd ui && npm run test

# Production commands
prod:
	docker-compose up -d

prod-build:
	docker-compose up --build -d

prod-logs:
	docker-compose logs -f

prod-stop:
	docker-compose down

# Production with Nginx
prod-nginx:
	docker-compose --profile production up --build -d

prod-nginx-logs:
	docker-compose --profile production logs -f

# Testing commands
test:
	ENVIRONMENT=test python -m pytest tests/ -v

test-cov:
	ENVIRONMENT=test python -m pytest tests/ --cov=. --cov-report=html

# Utility commands
ssl:
	./scripts/generate-ssl.sh

clean:
	docker-compose down -v
	docker-compose -f docker-compose.dev.yml down -v
	docker system prune -f
	docker volume prune -f

logs:
	docker-compose logs -f

# Database commands
db-migrate:
	docker-compose exec api alembic upgrade head

db-rollback:
	docker-compose exec api alembic downgrade -1

db-reset:
	docker-compose down -v
	docker-compose up postgres -d
	sleep 10
	docker-compose exec postgres psql -U postgres -d ideahub -f /docker-entrypoint-initdb.d/init.sql

db-migrate-dev:
	docker-compose -f docker-compose.dev.yml exec api alembic upgrade head

db-rollback-dev:
	docker-compose -f docker-compose.dev.yml exec api alembic downgrade -1

db-generate-migration:
	docker-compose exec api alembic revision --autogenerate -m "$(message)"

db-generate-migration-dev:
	docker-compose -f docker-compose.dev.yml exec api alembic revision --autogenerate -m "$(message)"

# i18n commands
i18n-extract:
	@echo "Extracting translatable strings..."
	@find . -name "*.py" -exec grep -l "get_text\|t(" {} \; | xargs python -c "import re, sys; print('\n'.join(set(re.findall(r'get_text\([\"']([^\"']+)[\"']', open(f).read()) for f in sys.argv[1:])))"

i18n-compile:
	@echo "Compiling i18n files..."
	@cd locales && for file in *.json; do echo "Compiled $$file"; done

# Health checks
health:
	curl -f http://localhost:8000/health

health-detailed:
	curl -f http://localhost:8000/health/detailed

# Shell access
shell:
	docker-compose exec api bash

shell-dev:
	docker-compose -f docker-compose.dev.yml exec api bash

# Database shell
db-shell:
	docker-compose exec postgres psql -U postgres -d ideahub
