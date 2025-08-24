# Production-ready authorization predicates
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

def is_authenticated(req) -> bool:
    """Check if the subject is authenticated."""
    try:
        return bool(getattr(req.subject, "is_authenticated", False))
    except Exception as e:
        logger.error(f"Authentication check failed: {e}")
        return False

def is_admin(req) -> bool:
    """Check if the subject has admin privileges."""
    try:
        return bool(getattr(req.subject, "is_admin", False))
    except Exception as e:
        logger.error(f"Admin check failed: {e}")
        return False

def has_role(req, role: str) -> bool:
    """Check if the subject has a specific role."""
    try:
        roles = getattr(req.subject, "roles", [])
        return role in roles
    except Exception as e:
        logger.error(f"Role check failed: {e}")
        return False

def is_workspace_member(req, workspace_id: int) -> bool:
    """Check if the subject is a member of the specified workspace."""
    try:
        workspace_memberships = getattr(req.subject, "workspace_memberships", [])
        return workspace_id in workspace_memberships
    except Exception as e:
        logger.error(f"Workspace membership check failed: {e}")
        return False

def is_resource_owner(req) -> bool:
    """Check if the subject owns the resource."""
    try:
        subject_id = getattr(req.subject, "id", None)
        resource_owner_id = getattr(req.resource, "owner_id", None)
        return subject_id == resource_owner_id
    except Exception as e:
        logger.error(f"Resource ownership check failed: {e}")
        return False

def is_public_resource(req) -> bool:
    """Check if the resource is public."""
    try:
        return bool(getattr(req.resource, "public", False))
    except Exception as e:
        logger.error(f"Public resource check failed: {e}")
        return False

def action_matches(req, action: str) -> bool:
    """Check if the request action matches the specified action."""
    try:
        return req.action == action
    except Exception as e:
        logger.error(f"Action match check failed: {e}")
        return False
