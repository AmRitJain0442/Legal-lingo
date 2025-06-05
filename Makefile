.PHONY: help install-deps db-start db-stop db-clean db-restart server dev db-logs clean

help:
	@echo "Available targets:"
	@echo "  install-deps      - Install dependencies using uv"
	@echo "  db-start     - Start PostgreSQL databases"
	@echo "  db-stop      - Stop databases"
	@echo "  db-clean     - Stop databases and remove all data"
	@echo "  db-restart   - Restart databases"
	@echo "  db-logs      - Show database logs"
	@echo "  server       - Start the FastAPI server"
	@echo "  dev          - Start server in development mode with auto-reload"
	@echo "  clean        - Clean up containers and volumes"
	@echo "  setup        - Full setup: install deps and start databases"

install-deps:
	uv sync --frozen
	@echo "Dependencies installed successfully"

db-start:
	docker compose up -d postgres-db 
	@echo "Waiting for databases to be ready..."
	@sleep 10
	@echo "Databases started successfully"

db-stop:
	docker compose stop postgres-db 
	@echo "Databases stopped"
	
db-clean:
	docker compose down -v
	docker volume rm postgres-db-volume 2>/dev/null || true
	@echo "Databases stopped and data cleaned"

db-logs:
	docker compose logs -f postgres-db

db-restart: db-stop db-start

server: db-start
	uv run main.py

dev: db-start
	uv run main.py --reload 

clean:
	docker compose down
	docker system prune -f

setup: install-deps db-start
	@echo "Setup complete - dependencies installed and databases started"
