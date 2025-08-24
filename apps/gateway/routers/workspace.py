from fastapi import APIRouter, HTTPException, Header, Depends, Request
from typing import Optional
from domains.workspace.repository import WorkspaceRepository
from domains.workspace.service import WorkspaceService
from mappers.workspace_mapper import map_workspace
from ideahub_platform.authz.registry import get_engine
from ideahub_platform.authz.engine import Request as AuthRequest
from ideahub_platform.common.errors import AuthorizationError, NotFoundError
from ideahub_platform.common.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/workspaces")

repo = WorkspaceRepository()
svc = WorkspaceService(repo)
authz_engine = get_engine()

@router.get("/{workspace_id}")
def get_workspace(
    workspace_id: int, 
    request: Request,
    x_debug_auth: Optional[str] = Header(None)
):
    """Get workspace by ID with authorization."""
    
    # Create subject object for authorization
    is_authenticated = x_debug_auth != "anon"
    subject = type('Subject', (), {
        'is_authenticated': is_authenticated,
        'id': 1,  # Mock user ID
        'roles': ['user'],
        'is_admin': False
    })()
    
    # Create authorization request
    auth_request = AuthRequest(
        subject=subject,
        action="WORKSPACE_READ",
        resource={"id": workspace_id},
        ctx={"request_id": getattr(request.state, "request_id", "unknown")}
    )
    
    # Check authorization
    decision = authz_engine.decide(auth_request)
    if not decision.allow:
        logger.warning("Access denied", extra_fields={
            "workspace_id": workspace_id,
            "reason": decision.reason,
            "request_id": getattr(request.state, "request_id", "unknown")
        })
        raise AuthorizationError(
            message=f"Access denied: {decision.reason}",
            error_code="ACCESS_DENIED",
            details={"workspace_id": workspace_id, "reason": decision.reason}
        )
    
    # Get workspace data
    ws = svc.get(workspace_id)
    if not ws:
        logger.warning("Workspace not found", extra_fields={
            "workspace_id": workspace_id,
            "request_id": getattr(request.state, "request_id", "unknown")
        })
        raise NotFoundError(
            message="Workspace not found",
            error_code="WORKSPACE_NOT_FOUND",
            details={"workspace_id": workspace_id}
        )
    
    logger.info("Workspace retrieved", extra_fields={
        "workspace_id": workspace_id,
        "request_id": getattr(request.state, "request_id", "unknown")
    })
    
    return map_workspace(ws).model_dump()
