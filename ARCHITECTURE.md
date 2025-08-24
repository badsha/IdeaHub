# IdeaHub Architecture Overview

This document provides a high-level overview of the current codebase architecture, its layers, key modules, and notable observations discovered during a repository scan.

## Top-Level Structure

- apps/
  - gateway/: FastAPI application (API gateway) exposing HTTP endpoints via modular routers
- domains/: Domain layer with repositories and services for business logic
- ideahub_platform/: Platform/infrastructure layer (DB, models, authz, reporting, i18n, logging, common errors)
- api_models/: Public-facing API schemas/data structures and DTOs
- mappers/: Mapping utilities between domain models and API models
- tests/: Contract and unit tests
- ui/: Frontend (React + Vite) SPA

## Runtime Layers and Responsibilities

1. Presentation/API Layer (FastAPI)
   - Entry point: apps/gateway/main.py
     - Assembles the FastAPI app and includes routers: health, workspace, community, idea, search, reporting.
   - Routers: apps/gateway/routers/
     - health.py: Basic and detailed health checks, readiness endpoint. Pulls DB health and system metrics. Uses i18n for messages.
     - workspace.py: Authorization-guarded workspace retrieval. Delegates to domain service and maps results with mappers.
     - community.py, idea.py, search.py: Simple endpoints (stubs for now).
     - reporting.py: Rich reporting endpoints relying on ReportingService and ReportingDataProvider.

2. Domain Layer (Business Logic)
   - domains/workspace/{repository.py, service.py}
     - Repository: In-memory store for workspaces (Milestone 2), keyed by ID.
     - Service: Thin wrapper delegating to repository; used by workspace router.
   - Other domains (campaign, community, idea, member): Placeholders or partial implementations.

3. Platform/Infrastructure Layer
   - Database (ideahub_platform/db)
     - base.py: Central DB configuration using SQLAlchemy with PostgreSQL (QueuePool, pre_ping, pooling controls). Provides:
       - DatabaseManager: engine/session management, health_check, and a get_db dependency.
       - Base: Declarative base for ORM models.
       - get_db(): FastAPI dependency yielding a session via contextmanager.
     - models/: ORM models (e.g., Workspace).
     - migrations/: Alembic setup and example migration.
   - Authorization (ideahub_platform/authz)
     - engine.py: Tiny policy engine with Decision, Request, Policy, and Engine classes.
     - predicates.py: Common predicates such as is_authenticated, is_admin, etc.
     - registry.py: Predefined policies and a singleton Engine instance (get_engine(), reload_policies()).
       - Notable policy: allows WORKSPACE_READ for authenticated users; denies unauthenticated by default.
   - Reporting (ideahub_platform/reporting)
     - services.py: Orchestrates reporting computations and aggregates.
     - data_provider.py: Data access layer for reporting (SQL queries / ORM usage expected).
     - processors.py: Composable processors (IdeaStatProcessor, CommunityStatProcessor, etc.).
   - Common utilities
     - i18n/: Translation manager and locale files.
     - common/errors.py: Application error taxonomy + mapping to HTTPException (handle_exception).
     - common/logging.py: Logger factory.
     - common/tenant.py: Workspace/tenant detection helpers.
   - Events (ideahub_platform/events)
     - bus.py and event_types.py present; infrastructure for event-driven extensions.

4. API Models and Mappers
   - api_models/*: Pydantic models for shaping responses and requests.
   - mappers/*: Simple mapping functions between domain objects and API schemas (e.g., map_workspace).

## Data Flow: Example (GET /workspaces/{id})

1. Request hits apps/gateway/routers/workspace.py::get_workspace
2. Subject is constructed from headers (X-Debug-Auth). If header equals "anon", subject.is_authenticated = False.
3. Authorization request created (action WORKSPACE_READ, resource with workspace_id).
4. Engine decides based on policies in ideahub_platform/authz/registry.py.
   - Authenticated => allow; unauthenticated => deny (access_denied_unauthenticated).
5. If allowed: WorkspaceService.get(id) -> WorkspaceRepository.get_by_id(id) (in-memory).
6. If found: map_workspace(ws).model_dump() returned to client.
7. If not found: NotFoundError raised.

## Health and Observability

- Detailed health endpoint checks DB connectivity via DatabaseManager.health_check() and reports system metrics (CPU, memory, disk) and process stats.
- Logging uses structured extra_fields for request_id and metrics.
- Errors: common/errors.py provides a mechanism to convert domain errors into HTTPException, but routers currently raise custom exceptions directly; a global exception handler integration would be needed in app setup to uniformly apply handle_exception.

## Notable Observations / Potential Improvements

1. Duplicate Package Tree
   - There appears to be a duplicated package namespace under ideahub_platform/ideahub_platform/* alongside ideahub_platform/*.
   - Risk: Import ambiguity/shadowing in certain packaging or runtime contexts. Consider consolidating to a single package path and adjusting imports/setup.

2. Error Handling Integration
   - While a robust error abstraction exists (IdeaHubError types + handle_exception), the FastAPI app does not register a global exception handler. Consider adding app.add_exception_handler(IdeaHubError, ...) to ensure consistent HTTP mapping and messages.

3. Authorization Subject Modeling
   - Routers construct an ad-hoc Subject using type(). As auth matures, consider a dedicated subject/user model and an authentication layer to populate it (e.g., dependency for current_user).

4. Database Availability in Dev/Test
   - health/detailed uses a real PostgreSQL connection string by default. Local dev and tests may fail if DB is not up. For unit tests, consider using a SQLite URL or dependency overrides.

5. Domain Implementations
   - Current domain services (other than workspace) are stubs; incrementally fill repositories/services and align API routers with domain logic.

6. Testing
   - tests/ include contract tests for endpoints and unit tests for authz. Ensure test infra spins necessary services or uses dependency overrides/mocks for DB.

7. Internationalization
   - health endpoint returns a localized message using accept-language. Ensure locales coverage for user-facing strings.

## Summary

- The project follows a clean layering: API (FastAPI) -> Domain (services/repositories) -> Platform (DB/Authz/Reporting/Common).
- Authorization is centralized and policy-based; data access standardized via SQLAlchemy with a connection manager.
- Reporting is a separate sub-module with processors and a service abstraction.
- Key housekeeping: remove duplicate ideahub_platform tree and wire global error handling into FastAPI app.
