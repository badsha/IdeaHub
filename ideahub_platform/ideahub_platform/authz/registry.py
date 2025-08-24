from .engine import Engine, Policy
from .predicates import is_authenticated

policies = [
    Policy("allow", [is_authenticated, lambda r: r.action == "WORKSPACE_READ"], reason="workspace_read_authenticated"),
    Policy("deny",  [lambda r: r.action == "WORKSPACE_READ"], reason="workspace_read_denied"),
]

authz_engine = Engine(policies)
