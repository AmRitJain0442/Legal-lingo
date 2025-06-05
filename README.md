# LegalLingo Backend

## Technology Stack
- **Backend Framework**: FastAPI 
- **Database**: PostgreSQL (primary)
- **ORM**: SQLAlchemy
- **Database Migrations**: Alembic
- **Package Manager**: UV (recommended)
- **Development Tools**: Ruff (linting/formatting)

## Prerequisites
Before getting started, ensure you have the following installed:

- Python 
- Docker and Docker Compose
- UV package manager (recommended) or pip
- Git

### Installing UV (Recommended)

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
For Windows installation instructions, see: https://docs.astral.sh/uv/getting-started/installation/

## Quick Start

### 1. Clone the Repository

### 2. Environment Setup

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit the `.env` file with your preferred settings. The default values work for local development.

### 3. Complete Setup

Use the provided Makefile for automated setup:

```bash
make setup
```

This command will:
- Install all Python dependencies
- Start the PostgreSQL database container
- Wait for the database to be ready

### 4. Start the Development Server

```bash
make dev
```

The API will be available at:
- Main API: http://localhost:10000
- Interactive API Documentation (Swagger): http://localhost:10000/docs
- Alternative Documentation (ReDoc): http://localhost:10000/redoc
- Health Check: http://localhost:10000/api/health

## Available Make Commands

The project includes a comprehensive Makefile for common operations:

```bash
make help              # Show all available commands
make install-deps      # Install Python dependencies using UV
make db-start         # Start PostgreSQL database container
make db-stop          # Stop database container
make db-clean         # Stop database and remove all data
make db-restart       # Restart database container
make db-logs          # View database container logs
make server           # Start the FastAPI server in production mode
make dev              # Start server in development mode with auto-reload
make clean            # Clean up Docker containers and volumes
make setup            # Complete setup (install deps + start database)
```

## Database Setup

### Database Migrations

The project uses Alembic for database migrations:

```bash
# Generate a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

## API Documentation

Once the server is running, you can access the API documentation:

- **Swagger UI**: http://localhost:10000/docs
- **ReDoc**: http://localhost:10000/redoc
- **OpenAPI JSON**: http://localhost:10000/openapi.json

## Environment Variables

Key environment variables (see `.env.example` for all options):

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | LegalLingo API |
| `APP_VERSION` | Application version | 1.0.0 |
| `DEBUG` | Enable debug mode | false |
| `POSTGRES_USER` | PostgreSQL username | legallingo-backend |
| `POSTGRES_PASSWORD` | PostgreSQL password | legallingo-backend-password |
| `POSTGRES_DB` | PostgreSQL database name | legallingo |
| `POSTGRES_HOST` | PostgreSQL host | localhost |
| `POSTGRES_PORT` | PostgreSQL port | 5432 |
| `API_PREFIX` | API prefix for all routes | /api |
| `SQL_ECHO` | Enable SQL query logging | false |

## Development

### Project Structure

```
legallingo/
├── app/
│   ├── apis/           # API routes and endpoints
│   │   ├── health/     # Health check endpoints
│   │   └── router.py   # Main API router
│   ├── core/           # Core application logic
│   │   ├── config.py   # Configuration management
│   │   ├── db/         # Database setup and connections
│   │   └── utils/      # Utility functions and response models
│   └── __init__.py
├── migrations/         # Alembic database migrations
├── db-metadata/        # SmartQnA Database schema and metadata
├── docker-compose.yml  # Docker services configuration
├── main.py            # Application entry point
├── pyproject.toml     # Project dependencies and metadata
├── Makefile           # Automation commands
└── README.md          # This file
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Ensure PostgreSQL container is running: `docker ps`
   - Check database logs: `make db-logs`
   - Verify environment variables in `.env`

### Logs and Debugging

- Application logs: Check console output when running the server
- Database logs: `make db-logs`
- Enable SQL echo: Set `SQL_ECHO=true` in `.env`
- Enable debug mode: Set `DEBUG=true` in `.env`
