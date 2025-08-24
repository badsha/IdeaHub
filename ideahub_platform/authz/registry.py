from .engine import Engine, Policy
from .predicates import (
    is_authenticated, is_admin, has_role, is_workspace_member,
    is_resource_owner, is_public_resource, action_matches
)
import logging

logger = logging.getLogger(__name__)

# Production-ready authorization policies
policies = [
    # Admin policies (highest priority)
    Policy(
        "allow", 
        [is_admin], 
        reason="admin_access", 
        priority=100
    ),
    
    # Workspace policies
    Policy(
        "allow", 
        [is_authenticated, lambda r: action_matches(r, "WORKSPACE_READ")], 
        reason="workspace_read_authenticated", 
        priority=50
    ),
    Policy(
        "allow", 
        [is_authenticated, lambda r: action_matches(r, "WORKSPACE_WRITE")], 
        reason="workspace_write_authenticated", 
        priority=50
    ),
    
    # Community policies
    Policy(
        "allow", 
        [is_authenticated, lambda r: action_matches(r, "COMMUNITY_READ")], 
        reason="community_read_authenticated", 
        priority=40
    ),
    Policy(
        "allow", 
        [is_public_resource, lambda r: action_matches(r, "COMMUNITY_READ")], 
        reason="community_read_public", 
        priority=35
    ),
    
    # Idea policies
    Policy(
        "allow", 
        [is_authenticated, lambda r: action_matches(r, "IDEA_READ")], 
        reason="idea_read_authenticated", 
        priority=30
    ),
    Policy(
        "allow", 
        [is_public_resource, lambda r: action_matches(r, "IDEA_READ")], 
        reason="idea_read_public", 
        priority=25
    ),
    Policy(
        "allow", 
        [is_authenticated, is_resource_owner, lambda r: action_matches(r, "IDEA_WRITE")], 
        reason="idea_write_owner", 
        priority=30
    ),
    
    # Search policies
    Policy(
        "allow", 
        [is_authenticated, lambda r: action_matches(r, "SEARCH")], 
        reason="search_authenticated", 
        priority=20
    ),
    
    # Deny policies (lowest priority)
    Policy(
        "deny", 
        [lambda r: action_matches(r, action) for action in ["WORKSPACE_READ", "COMMUNITY_READ", "IDEA_READ", "SEARCH"]], 
        reason="access_denied_unauthenticated", 
        priority=10
    ),
]

authz_engine = Engine(policies)

def get_engine() -> Engine:
    """Get the authorization engine instance."""
    return authz_engine

def reload_policies(new_policies: list) -> None:
    """Reload policies (useful for dynamic policy updates)."""
    global authz_engine, policies
    policies = new_policies
    authz_engine = Engine(policies)
    logger.info("Authorization policies reloaded")
