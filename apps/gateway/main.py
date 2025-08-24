from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from apps.gateway.routers import health, workspace, community, idea, search, reporting
from ideahub_platform.common.errors import (
    IdeaHubError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    NotFoundError,
    ConflictError,
)

app = FastAPI(title="IdeaScale Python API", version="0.1.0")

# Global exception handler to normalize IdeaHub errors to HTTP responses with string detail
@app.exception_handler(IdeaHubError)
async def ideahub_error_handler(request: Request, exc: IdeaHubError):
    status_code = 500
    if isinstance(exc, AuthenticationError):
        status_code = 401
    elif isinstance(exc, AuthorizationError):
        status_code = 403
    elif isinstance(exc, ValidationError):
        status_code = 400
    elif isinstance(exc, NotFoundError):
        status_code = 404
    elif isinstance(exc, ConflictError):
        status_code = 409

    # Convert error_code to snake_case lowercase string for client contracts
    code = (exc.error_code or exc.__class__.__name__).strip()
    code = code.replace(" ", "_").lower()
    return JSONResponse(status_code=status_code, content={"detail": code})

app.include_router(health.router)
app.include_router(workspace.router)
app.include_router(community.router)
app.include_router(idea.router)
app.include_router(search.router)
app.include_router(reporting.router)
