# Authorization DSL for policy definition
from typing import Any, Dict, List, Callable
from .engine import Request, Policy
import logging

logger = logging.getLogger(__name__)

class PolicyBuilder:
    """Builder pattern for creating authorization policies."""
    
    def __init__(self):
        self._effect = "allow"
        self._predicates = []
        self._reason = "policy"
        self._priority = 0
        
    def allow(self) -> 'PolicyBuilder':
        """Set policy effect to allow."""
        self._effect = "allow"
        return self
        
    def deny(self) -> 'PolicyBuilder':
        """Set policy effect to deny."""
        self._effect = "deny"
        return self
        
    def when(self, predicate: Callable[[Request], bool]) -> 'PolicyBuilder':
        """Add a predicate condition."""
        self._predicates.append(predicate)
        return self
        
    def reason(self, reason: str) -> 'PolicyBuilder':
        """Set the policy reason."""
        self._reason = reason
        return self
        
    def priority(self, priority: int) -> 'PolicyBuilder':
        """Set the policy priority."""
        self._priority = priority
        return self
        
    def build(self) -> Policy:
        """Build the policy."""
        return Policy(
            effect=self._effect,
            when=self._predicates,
            reason=self._reason,
            priority=self._priority
        )

def policy() -> PolicyBuilder:
    """Create a new policy builder."""
    return PolicyBuilder()

# DSL helper functions
def authenticated() -> Callable[[Request], bool]:
    """Check if user is authenticated."""
    from .predicates import is_authenticated
    return is_authenticated

def admin() -> Callable[[Request], bool]:
    """Check if user is admin."""
    from .predicates import is_admin
    return is_admin

def has_role(role: str) -> Callable[[Request], bool]:
    """Check if user has specific role."""
    from .predicates import has_role as has_role_predicate
    return lambda req: has_role_predicate(req, role)

def action_is(action: str) -> Callable[[Request], bool]:
    """Check if request action matches."""
    from .predicates import action_matches
    return lambda req: action_matches(req, action)

def resource_owner() -> Callable[[Request], bool]:
    """Check if user owns the resource."""
    from .predicates import is_resource_owner
    return is_resource_owner

def public_resource() -> Callable[[Request], bool]:
    """Check if resource is public."""
    from .predicates import is_public_resource
    return is_public_resource

# Example usage:
# workspace_read_policy = (
#     policy()
#     .allow()
#     .when(authenticated())
#     .when(action_is("WORKSPACE_READ"))
#     .reason("workspace_read_authenticated")
#     .priority(50)
#     .build()
# )
