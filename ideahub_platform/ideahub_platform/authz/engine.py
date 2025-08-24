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
