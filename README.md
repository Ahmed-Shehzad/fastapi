# FastAPI Task Management API

A modern, production-ready FastAPI application implementing Clean Architecture with CQRS pattern, PostgreSQL database, and Docker support.

## 🏗️ Architecture

- **Clean Architecture**: Separation of concerns with Domain, Application, Infrastructure, and Presentation layers
- **CQRS Pattern**: Command Query Responsibility Segregation with Mediator pattern
- **Domain-Driven Design**: Proper domain modeling with entities, value objects, and aggregates
- **Dependency Injection**: FastAPI's built-in DI container for loose coupling

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- pip (Python package manager)

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd fastapi
```

### 2. Start with Docker (Recommended)

```bash
# Start PostgreSQL and the application
./start.sh
```

### 3. Manual Setup

```bash
# Start PostgreSQL container
docker-compose up -d postgres

# Install dependencies
pip install -r requirements.txt

# Start the application
cd app && uvicorn main:app --reload
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://taskuser:taskpassword@localhost:5432/taskdb

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

### Docker Services

- **PostgreSQL**: `localhost:5432`
  - Database: `taskdb`
  - Username: `taskuser`
  - Password: `taskpassword`

- **PgAdmin** (optional): `localhost:5050`
  - Email: `admin@admin.com`
  - Password: `admin`

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛠️ Available Endpoints

### Tasks

- `POST /api/tasks/` - Create a new task
- `GET /` - Health check

### Example Request

```json
POST /api/tasks/
{
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API docs",
  "priority": 2,
  "completed": false
}
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## 🏭 Production Deployment

### Docker Production

```bash
# Build production image
docker build -t fastapi-tasks .

# Run with production settings
ENVIRONMENT=production docker-compose up -d
```

### Environment Variables for Production

```bash
ENVIRONMENT=production
DATABASE_URL=postgresql://user:password@your-db-host:5432/dbname
SECRET_KEY=your-super-secret-key
```

## 📦 Project Structure

```
app/
├── main.py                     # FastAPI application entry point
└── src/
    ├── application/            # Application layer (CQRS commands/handlers)
    │   └── tasks/
    │       ├── commands/       # Command definitions
    │       └── command_handlers/ # Command handlers
    ├── core/                   # Core functionality
    │   ├── config/             # Configuration management
    │   ├── mediator/           # Mediator pattern implementation
    │   ├── utils/              # Utility functions
    │   └── dependencies.py     # DI container setup
    ├── domain/                 # Domain layer
    │   └── aggregates/
    │       ├── entities/       # Domain entities
    │       ├── value_objects/  # Value objects
    │       └── services/       # Domain services
    ├── infrastructure/         # Infrastructure layer
    │   ├── database/           # Database configuration
    │   └── repositories/       # Data access repositories
    └── presentation/           # Presentation layer
        └── api/                # API routes and controllers
```

## 🎯 Features

- ✅ Clean Architecture implementation
- ✅ CQRS with Mediator pattern
- ✅ PostgreSQL with Docker
- ✅ SQLModel for type-safe database operations
- ✅ Pydantic for data validation
- ✅ Environment-based configuration
- ✅ Connection pooling
- ✅ Health checks
- ✅ API documentation
- 🔄 Unit tests (coming soon)
- 🔄 Integration tests (coming soon)
- 🔄 Authentication & Authorization (coming soon)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
