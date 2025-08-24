# IdeaHub - Production-Ready API Platform

A modular-monolith FastAPI application for idea management and collaboration, built with production-ready features including PostgreSQL, Redis, Docker, and comprehensive monitoring.

## 🧭 TL;DR: Start & Test

- Prerequisites: Python 3.11+ (or 3.12 for local), Node 18+ (for UI), Docker (optional), Make, and optionally Poetry.
- Backend (local, no Docker):
  - Using Poetry: `pip install poetry && poetry install`
  - Or using pip: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
  - Run tests: `ENVIRONMENT=test python -m pytest tests/ -q`
  - Start API: `uvicorn apps.gateway.main:app --reload --port 8000`
  - Try it:
    - `curl http://localhost:8000/health` → {"status":"ok", ...}
    - `curl http://localhost:8000/workspaces/1` → workspace JSON
    - `curl -H 'X-Debug-Auth: anon' http://localhost:8000/workspaces/1` → 403 with detail access_denied
    - `curl http://localhost:8000/workspaces/999` → 404 with detail workspace_not_found
- Docker (full stack):
  - Dev: `docker-compose -f docker-compose.dev.yml up --build`
  - Prod: `docker-compose up --build -d`
  - Makefile shortcuts: `make dev-build`, `make test`, `make db-migrate-dev`

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **React UI** - Modern, responsive frontend with TypeScript and Tailwind CSS
- **PostgreSQL** - Production-ready database with proper indexing and full-text search (Docker-only)
- **Redis** - Caching and session storage
- **Docker** - Complete containerization with multi-stage builds
- **Nginx** - Reverse proxy with SSL, rate limiting, and security headers
- **Authorization** - ABAC (Attribute-Based Access Control) system
- **Structured Logging** - JSON-formatted logs with correlation IDs
- **Health Checks** - Comprehensive monitoring endpoints
- **Event Bus** - Asynchronous event processing
- **Database Migrations** - Alembic support for schema management
- **Internationalization** - Full i18n support for backend and frontend (EN/ES)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx (SSL)   │    │   FastAPI App   │    │   PostgreSQL    │
│   (Reverse      │◄──►│   (API Layer)   │◄──►│   (Database)    │
│    Proxy)       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Rate Limiting │    │   Event Bus     │    │   Full-Text     │
│   & Security    │    │   (Async)       │    │   Search        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🐳 Quick Start with Docker

### Development Environment

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd IdeaHub
   ```

2. **Start development environment:**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

3. **Access the application:**
   - Frontend UI: http://localhost:3000
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PgAdmin: http://localhost:8080 (admin@ideahub.com / admin)

### Production Environment

1. **Set environment variables:**
   ```bash
   export POSTGRES_PASSWORD=your_secure_password
   export REDIS_PASSWORD=your_redis_password
   export PGADMIN_EMAIL=your_email@example.com
   export PGADMIN_PASSWORD=your_pgadmin_password
   ```

2. **Start production environment:**
   ```bash
   docker-compose up --build
   ```

3. **With Nginx (production):**
   ```bash
   docker-compose --profile production up --build
   ```

## 🔧 Development Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- Node.js 18+ (for local UI development)
- **No PostgreSQL installation required** - runs in Docker containers only

### Local Development

1. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up database:**
   ```bash
   # Start PostgreSQL with Docker (recommended)
   docker-compose up postgres -d
   
   # Run database migrations
   make db-migrate-dev
   ```

3. **Run the application:**
   ```bash
   uvicorn apps.gateway.main:app --reload --port 8000
   ```

4. **Run tests:**
   ```bash
   # Backend tests
   ENVIRONMENT=test python -m pytest tests/ -v
   
   # Frontend tests
   cd ui && npm run test
   ```

## 📊 API Endpoints

### Core Endpoints

- `GET /health` - Health check
- `GET /health/detailed` - Detailed system metrics
- `GET /health/ready` - Kubernetes readiness probe

### Core API

- `GET /workspaces/{id}` - Get workspace
- `GET /communities/{id}` - Get community
- `GET /ideas/{id}` - Get idea
- `GET /search?q={query}` - Search ideas

### Analytics & Reporting API

- `GET /reporting/workspace/{workspace_id}/statistics` - Get workspace statistics
- `GET /reporting/workspace/{workspace_id}/activity` - Get workspace activity logs
- `GET /reporting/workspace/{workspace_id}/daily-summary` - Get daily activity summary
- `POST /reporting/workspace/{workspace_id}/process-statistics` - Process statistics
- `POST /reporting/workspace/{workspace_id}/reset-statistics` - Reset statistics
- `GET /reporting/analytics/dashboard` - Get analytics dashboard data
- `POST /reporting/activity/log` - Log activity for reporting

### Authentication

Use the `X-Debug-Auth` header for testing:
- `X-Debug-Auth: anon` - Simulate anonymous user (will be denied)
- No header - Simulate authenticated user (will be allowed)

## 🗄️ Database Schema

The application uses PostgreSQL with the following main tables:

- **workspaces** - Top-level organizations
- **communities** - Groups within workspaces
- **campaigns** - Time-bound idea collection periods
- **members** - Users of the platform
- **ideas** - User-submitted ideas
- **workspace_members** - Many-to-many relationship

## 🔐 Authorization

The application implements ABAC (Attribute-Based Access Control) with:

- **Policies** - Rules that define access permissions
- **Predicates** - Functions that evaluate access conditions
- **Subjects** - Users with attributes (roles, permissions)
- **Resources** - Objects being accessed (workspaces, ideas)
- **Actions** - Operations being performed (read, write)

## 📈 Monitoring & Observability

### Health Checks

- **Basic Health**: `GET /health`
- **Detailed Health**: `GET /health/detailed` (includes system metrics)
- **Readiness**: `GET /health/ready` (for Kubernetes)

### Logging

- Structured JSON logging
- Request correlation IDs
- Performance metrics
- Error tracking

### Metrics

- Database connection pool status
- System resource usage
- API response times
- Error rates

## 🚀 Deployment

### Docker Deployment

1. **Build and run:**
   ```bash
   docker-compose up --build -d
   ```

2. **Scale the API:**
   ```bash
   docker-compose up --scale api=3 -d
   ```

### Kubernetes Deployment

1. **Create namespace:**
   ```bash
   kubectl create namespace ideahub
   ```

2. **Apply configurations:**
   ```bash
   kubectl apply -f k8s/
   ```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment (development/production) | development |
| `DATABASE_URL` | PostgreSQL connection string | postgresql://postgres:password@localhost:5432/ideahub |
| `DB_POOL_SIZE` | Database connection pool size | 10 |
| `DB_MAX_OVERFLOW` | Database connection pool overflow | 20 |
| `LOG_LEVEL` | Logging level | INFO |
| `POSTGRES_PASSWORD` | PostgreSQL password | password |
| `REDIS_PASSWORD` | Redis password | redis_password |
| `DEFAULT_LOCALE` | Default language for i18n | en |

## 🧪 Testing

### Run Tests

```bash
# All tests
ENVIRONMENT=test python -m pytest tests/ -v

# Specific test categories
ENVIRONMENT=test python -m pytest tests/unit/ -v
ENVIRONMENT=test python -m pytest tests/contract/ -v

# With coverage
ENVIRONMENT=test python -m pytest tests/ --cov=. --cov-report=html
```

### Test Categories

- **Unit Tests**: Test individual components
- **Contract Tests**: Test API endpoints
- **Integration Tests**: Test component interactions

## 🔧 Configuration

### Database Configuration

The application uses PostgreSQL exclusively in Docker containers:

- **Development**: PostgreSQL with debug logging and hot reloading
- **Production**: Optimized connection pooling and monitoring
- **Migrations**: Automatic Alembic migrations on startup

### Internationalization (i18n)

The application supports multiple languages:

- **Backend**: Python i18n with JSON locale files
- **Frontend**: React i18next with automatic language detection
- **Supported Languages**: English (en), Spanish (es)
- **Locale Files**: Located in `locales/` directory

### Multi-Tenancy Support

The application supports multi-tenancy through workspace URL-based routing:

- **Workspace URLs**: Each workspace has a unique URL identifier
- **Tenant Resolution**: Automatic workspace discovery from request URLs
- **Isolation**: Complete data isolation between workspaces
- **URL Pattern**: `/workspace/{workspace_url}/...`

### Analytics & Reporting

Comprehensive analytics and reporting system:

- **Real-time Statistics**: Workspace, community, and idea metrics
- **Activity Tracking**: Detailed activity logs for all user actions
- **Batch Processing**: Background processors for computing statistics
- **Dashboard**: Interactive analytics dashboard with charts and metrics
- **API Endpoints**: RESTful API for accessing analytics data
- **Data Provider**: Flexible data provider for custom queries

### Logging Configuration

- **Development**: Console output with debug information
- **Production**: Structured JSON logging with correlation IDs

## 📚 Documentation

- **API Documentation**: Available at `/docs` when running
- **Code Documentation**: Inline docstrings and type hints
- **Architecture**: See architecture diagram above

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## 🔄 Roadmap

- [ ] Real-time notifications
- [ ] Advanced search with filters
- [ ] File upload support
- [ ] Email notifications
- [x] ~~Mobile API~~ (UI is mobile-friendly)
- [x] Analytics dashboard
- [x] Multi-tenancy support
