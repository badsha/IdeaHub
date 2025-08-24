AI Executor Brief: Scaffold and Implement the Python Rewrite (Single File, Copy-Paste Ready)

Purpose
- This is a self-contained instruction file for an AI coding assistant (e.g., Junie, JetBrains AI Assistant, GitHub Copilot Chat) to bootstrap a brand-new Python repository and deliver a runnable app with tests for Milestone 1-2.
- Paste this entire file into the AI inside an empty Python project folder. The AI should follow it verbatim.

Executive Summary
- Build a modular-monolith FastAPI application with:
  - platform/authz: policy engine (ABAC) and minimal policies
  - platform/db: SQLAlchemy base and connection
  - api_models: Pydantic v2 DTOs
  - domains: repository interfaces and simple services
  - apps/gateway: FastAPI app/routers
  - tests: unit and contract tests
- Milestone 1: Bootstrap, health check, basic authz engine, DTOs, DB base, skeleton routers, tests.
- Milestone 2: Read-only endpoints for workspace/community/idea/search using in-memory or stub repos with ABAC filtering, plus tests.

Important Domain Entities to Consider (carry-over from Java domain)
- Stages and stage-configurations: model minimal Stage/FunctionalStage DTOs and loaders when implementing workflows later.
- Groups: include visible groups at workspace and community scope.
- Group memberships: consider member-to-group relationships for visibility and permissions where applicable.
- Group assignments: include admin and moderation assignments (community-level and campaign-level) as part of future authorization decisions.
- Note: For Milestones 1-2, these can be represented with stub repositories and simple data structures, but they must be acknowledged in design to avoid rework.

Non-Goals
- No full feature parity with the legacy Java app yet.
- No complex background jobs, no real SSO, no advanced moderation. Keep it minimal but extensible.

Hard Requirements
- Language/Runtime: Python 3.11+
- Web: FastAPI + Uvicorn
- Models: Pydantic v2
- ORM/Migrations: SQLAlchemy 2.x + Alembic (migrations may be stubbed initially)
- Observability: Structured JSON logs (basic), Prometheus client dependency present (no custom metrics required yet)
- Tests: pytest, FastAPI TestClient, basic unit and contract tests must pass
- Lint/Format: Ruff + Black config present

Directory Layout (create exactly)
- pyproject.toml (or requirements.txt if using pip). Prefer Poetry with pyproject.
- apps/
  - gateway/
    - main.py
    - routers/
      - health.py
      - workspace.py
      - community.py
      - idea.py
      - search.py
- platform/
  - authz/
    - engine.py
    - predicates.py
    - registry.py
    - dsl.py (optional placeholder)
  - db/
    - base.py
    - models/ (stub files ok)
    - migrations/ (can be empty initially)
  - events/
    - bus.py (stub)
    - event_types.py (stub)
  - common/
    - errors.py
    - logging.py
- domains/
  - workspace/
    - repository.py
    - service.py
  - community/
    - repository.py
    - service.py
  - campaign/
    - repository.py
    - service.py
  - idea/
    - repository.py
    - service.py
    - rules.py (stub)
    - commands.py (stub)
  - member/
    - repository.py (stub)
    - service.py (stub)
- api_models/
  - workspace.py
  - community.py
  - campaign.py
  - idea.py
  - member.py
  - label.py (stub)
  - stage.py (stub)
- mappers/
  - workspace_mapper.py
  - community_mapper.py
  - idea_mapper.py
- tests/
  - unit/platform/authz/test_policies.py
  - contract/apps/gateway/test_endpoints.py
  - test_health.py

Dependency Setup (Poetry preferred)
- Create pyproject.toml with these minimal constraints and dev tools:

  [tool.poetry]
  name = "ideascale-py"
  version = "0.1.0"
  description = "IdeaScale Python rewrite (modular monolith)"
  authors = ["Your Name <you@example.com>"]
  readme = "README.md"

  [tool.poetry.dependencies]
  python = ">=3.11,<3.13"
  fastapi = "^0.115.0"
  uvicorn = {extras = ["standard"], version = "^0.30.0"}
  pydantic = "^2.7.0"
  sqlalchemy = "^2.0.30"
  asyncpg = "^0.29.0"
  alembic = "^1.13.0"
  httpx = "^0.27.0"
  prometheus-client = "^0.20.0"
  opentelemetry-distro = "^0.48b0"
  opentelemetry-instrumentation-fastapi = "^0.48b0"
  opentelemetry-instrumentation-sqlalchemy = "^0.48b0"

  [tool.poetry.group.dev.dependencies]
  pytest = "^8.2.0"
  pytest-asyncio = "^0.23.0"
  ruff = "^0.5.0"
  black = "^24.4.0"
  mypy = "^1.10.0"

  [tool.ruff]
  line-length = 100

- If using pip instead: create requirements.txt with equivalent deps.

Scaffold: Minimal File Contents (exact templates)
1) apps/gateway/main.py

from fastapi import FastAPI
from apps.gateway.routers import health, workspace, community, idea, search

app = FastAPI(title="IdeaScale Python API", version="0.1.0")
app.include_router(health.router)
app.include_router(workspace.router)
app.include_router(community.router)
app.include_router(idea.router)
app.include_router(search.router)

2) apps/gateway/routers/health.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

3) platform/common/logging.py

import logging, sys, json
from typing import Any, Dict

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        return json.dumps(payload)

def configure_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=level, handlers=[handler])

4) platform/authz/engine.py

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

@dataclass
class Decision:
    allow: bool
    reason: str = "ok"

Predicate = Callable[["Request"], bool]

@dataclass
class Request:
    subject: Any
    action: str
    resource: Any
    ctx: Dict[str, Any]

class Policy:
    def __init__(self, effect: str, when: List[Predicate], reason: str = "policy"):
        self.effect = effect  # "allow" or "deny"
        self.when = when
        self.reason = reason

    def eval(self, req: Request) -> Optional[Decision]:
        if all(p(req) for p in self.when):
            return Decision(allow=(self.effect == "allow"), reason=self.reason)
        return None

class Engine:
    def __init__(self, policies: List[Policy]):
        self.policies = policies

    def decide(self, req: Request) -> Decision:
        last: Optional[Decision] = None
        for p in self.policies:
            d = p.eval(req)
            if d is not None:
                if d.allow:
                    return d
                last = d
        return last or Decision(False, "no_policy_matched")

5) platform/authz/predicates.py

# Simple starter predicates

def is_authenticated(req):
    return bool(getattr(req.subject, "is_authenticated", False))

6) platform/authz/registry.py

from .engine import Engine, Policy
from .predicates import is_authenticated

policies = [
    Policy("allow", [is_authenticated, lambda r: r.action == "WORKSPACE_READ"], reason="workspace_read_authenticated"),
    Policy("deny",  [lambda r: r.action == "WORKSPACE_READ"], reason="workspace_read_denied"),
]

authz_engine = Engine(policies)

7) platform/db/base.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:pass@localhost:5432/ideascale")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

8) api_models/workspace.py

from pydantic import BaseModel
from typing import Optional, List

class Workspace(BaseModel):
    id: int
    name: str
    public_default: bool = True
    features: Optional[List[str]] = None

9) api_models/community.py

from pydantic import BaseModel

class Community(BaseModel):
    id: int
    workspace_id: int
    name: str
    public: bool = True

10) api_models/idea.py

from pydantic import BaseModel
from typing import Optional

class Idea(BaseModel):
    id: int
    community_id: int
    campaign_id: Optional[int] = None
    author_member_id: Optional[int] = None
    title: str
    body: str
    visibility: str = "public"

11) mappers/workspace_mapper.py

from api_models.workspace import Workspace as WorkspaceDTO

def map_workspace(domain_obj) -> WorkspaceDTO:
    # domain_obj may be a dict for now
    return WorkspaceDTO(**domain_obj)

12) domains/workspace/repository.py

from typing import Optional, Dict

class WorkspaceRepository:
    def __init__(self):
        # In-memory store for Milestone 2
        self._by_id: Dict[int, Dict] = {
            1: {"id": 1, "name": "Public WS", "public_default": True, "features": []},
        }

    def get_by_id(self, ws_id: int) -> Optional[Dict]:
        return self._by_id.get(ws_id)

13) domains/workspace/service.py

from typing import Optional, Dict
from .repository import WorkspaceRepository

class WorkspaceService:
    def __init__(self, repo: WorkspaceRepository):
        self.repo = repo

    def get(self, ws_id: int) -> Optional[Dict]:
        return self.repo.get_by_id(ws_id)

14) apps/gateway/routers/workspace.py

from fastapi import APIRouter, HTTPException
from domains.workspace.repository import WorkspaceRepository
from domains.workspace.service import WorkspaceService
from mappers.workspace_mapper import map_workspace

router = APIRouter(prefix="/workspaces")

repo = WorkspaceRepository()
svc = WorkspaceService(repo)

@router.get("/{workspace_id}")
def get_workspace(workspace_id: int):
    ws = svc.get(workspace_id)
    if not ws:
        raise HTTPException(status_code=404, detail="workspace_not_found")
    return map_workspace(ws).model_dump()

15) apps/gateway/routers/community.py (stub OK)

from fastapi import APIRouter

router = APIRouter(prefix="/communities")

@router.get("/{community_id}")
def get_community(community_id: int):
    return {"id": community_id, "name": "Community", "workspace_id": 1, "public": True}

16) apps/gateway/routers/idea.py (stub OK)

from fastapi import APIRouter

router = APIRouter(prefix="/ideas")

@router.get("/{idea_id}")
def get_idea(idea_id: int):
    return {"id": idea_id, "community_id": 1, "title": "Hello", "body": "World"}

17) apps/gateway/routers/search.py (stub OK)

from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/search")
def search(q: str = Query(default="")):
    return {"q": q, "items": []}

18) tests/test_health.py

def test_health():
    from fastapi.testclient import TestClient
    from apps.gateway.main import app

    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

19) tests/contract/apps/gateway/test_endpoints.py

def test_workspace_endpoint():
    from fastapi.testclient import TestClient
    from apps.gateway.main import app

    client = TestClient(app)
    r = client.get("/workspaces/1")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == 1
    assert body["name"]

Milestones & Tasks
- Milestone 1 (Bootstrap) — Deliverables:
  1) All directories and files above created.
  2) Poetry install or pip install completes without errors.
  3) Uvicorn run command works: uvicorn apps.gateway.main:app --reload
  4) /health returns {"status": "ok"}.
  5) Tests pass: pytest .

- Milestone 2 (Read-only) — Deliverables:
  1) /workspaces/{id} returns mapped DTO from in-memory repo.
  2) /communities/{id}, /ideas/{id}, /search exist (stubs acceptable), with simple JSON outputs.
  3) Add a simple ABAC check placeholder: use authz_engine to allow WORKSPACE_READ only if a fake subject is_authenticated == True (for now, assume True). Prepare a function to build Request(subject, action, resource, ctx) and call Engine.decide; return 403 if denied.
  4) Extend tests to cover /workspaces/{id} happy path and a denied case when is_authenticated is False (you can pass a header X-Debug-Auth: anon to simulate anonymous and have the router enforce deny).

Run Config Suggestion
- Start server: uvicorn apps.gateway.main:app --reload --port 8000
- Browse: http://localhost:8000/health and http://localhost:8000/docs

Acceptance Criteria
- Repo contains the exact structure and minimal code above.
- `pytest` passes for provided tests.
- Server runs; endpoints respond as specified.
- Code quality setup exists (Ruff/Black config in pyproject or separate files).

Notes for the AI Assistant
- Keep imports relative to the created package structure; the project root should be a Sources Root.
- Avoid over-engineering: use in-memory repos to satisfy tests; add DB wiring only in base.py now.
- Write clean, small functions; keep authz predicates and policies simple at this stage.
- Prefer Pydantic model_dump for responses; avoid leaking internal structures.

Next Steps (after Milestone 2)
- Replace in-memory repos with SQLAlchemy models and a real Postgres connection.
- Implement policy registry for COMMUNITY_READ, IDEA_READ, and SEARCH filtering.
- Add mappers for community/idea and expand DTOs.
- Introduce Alembic migrations and CI with pytest + ruff + black.

UI/UX Layer Guidance (Optional but Recommended)
- Scope: This brief is API-first. However, to de-risk integration, provide a minimal UI plan and optional scaffold.
- Architecture:
  - Prefer a decoupled SPA that consumes the FastAPI endpoints. Suggested stack: React + Vite + TypeScript + React Router + TanStack Query.
  - Alternative: Server-rendered HTMX/FastAPI Jinja if you want ultra-minimal UI (good for admin-only tools).
- Folder suggestion (if adding UI now):
  - ui/
    - web/
      - src/
        - app/ (routes, layouts)
        - components/
        - features/ (workspace, community, idea, search)
        - lib/ (api client, auth context)
      - index.html, vite.config.ts, package.json
- Design system & theming:
  - Use a small component library (e.g., Radix UI + Tailwind) or Material UI. Define tokens for spacing, colors, typography.
  - Dark mode and accessibility (WCAG AA) baked in; use semantic HTML, focus states, ARIA where needed.
- State management:
  - Server cache via TanStack Query; local UI state via React Context or Zustand if necessary.
  - Keep URL as source of truth for filters/sorts; deep-linkable search pages.
- Navigation & IA:
  - Primary nav: Workspace -> Communities -> Campaigns -> Ideas.
  - Secondary actions: Submit Idea, Search, My Ideas, Admin (conditional by role).
- API integration:
  - Create a thin api client in ui/web/src/lib/api.ts using fetch or axios, mapping to the DTOs defined in api_models/*.
  - Auth header propagation (e.g., Authorization: Bearer <token>) once auth is enabled; for now, optional X-Debug-Auth used by Milestone 2 denial test.
- Performance & quality:
  - Code splitting per route, prefetch on hover, skeletons for loading.
  - E2E tests optional (Playwright/Cypress) after Milestone 2.

Member/User Management (Identity & Access Management)
- Goal: Establish a clear path for user identities, authentication, authorization, and account lifecycle with minimal viable implementation now and extensibility later.
- Terminology:
  - Member: an end-user participating in workspaces/communities/ideas.
  - User: synonymous with Member for now; later you may differentiate staff/admin operators.
- Current Milestone behavior:
  - No real auth provider; simulate identity with a subject object and header X-Debug-Auth: anon to force deny in ABAC.
  - DTOs already include author_member_id on Idea for future linkage.
- Recommended design:
  - Authentication:
    - Phase 1: Email magic link or username/password with JWT (FastAPI OAuth2PasswordBearer) and refresh tokens.
    - Phase 2: SSO via OAuth 2.0/OpenID Connect (Google, Azure AD, Okta). Store external subject identifiers.
  - Authorization:
    - Keep ABAC engine (platform/authz) as the single decision point.
    - Define attributes on subject (member): id, roles, workspace_roles, flags (is_authenticated, is_admin), org_id.
    - Resources expose attributes used in policies (workspace.public_default, community.public, idea.visibility).
    - Start with coarse-grained actions (WORKSPACE_READ, COMMUNITY_READ, IDEA_READ, SEARCH) and evolve to fine-grained if needed.
  - Account lifecycle:
    - Registration -> Email verification -> Active -> Suspended/Deleted.
    - GDPR/CCPA: soft-delete with erasure job; audit who performed changes.
  - Session management & security:
    - Short-lived access tokens, refresh rotation, cookie or Authorization header.
    - CSRF protection if using cookies; rate-limit login and sensitive endpoints.
  - Auditing & compliance:
    - Log auth events (login, logout, failed login), permission denies, admin changes with request IDs.
- Minimal API additions (optional now, safe stubs):
  - apps/gateway/routers/auth.py (login, refresh, me) returning stubbed user when enabled.
  - api_models/member.py: define Member DTO with id, email, display_name, roles: list[str], is_authenticated: bool.
  - domains/member/{repository.py,service.py}: in-memory member lookup by id/email.
- Policy examples to add later:
  - Allow COMMUNITY_READ if community.public or member is workspace member.
  - Allow IDEA_READ if idea.visibility == "public" or member is author or admin.
  - Deny otherwise with reason codes for observability.
- Admin/User management UI (future):
  - Admin screen to view members, assign roles per workspace, suspend/reactivate accounts.
  - Member profile page (name, avatar, preferences, notification settings).

Cross-References
- See CORE_OVERVIEW.md for architectural context and ADR-001 for modular-monolith rationale.
- TECH_STACK_EVALUATION_PYTHON.md discusses server-side choices; the UI suggestions above align with an API-first approach and can be implemented incrementally.
