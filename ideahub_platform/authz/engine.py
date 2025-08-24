from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class Decision:
    allow: bool
    reason: str = "ok"
    details: Optional[Dict[str, Any]] = None

Predicate = Callable[["Request"], bool]

@dataclass
class Request:
    subject: Any
    action: str
    resource: Any
    ctx: Dict[str, Any]

class Policy:
    def __init__(self, effect: str, when: List[Predicate], reason: str = "policy", priority: int = 0):
        self.effect = effect  # "allow" or "deny"
        self.when = when
        self.reason = reason
        self.priority = priority

    def eval(self, req: Request) -> Optional[Decision]:
        try:
            if all(p(req) for p in self.when):
                return Decision(
                    allow=(self.effect == "allow"), 
                    reason=self.reason,
                    details={"policy_priority": self.priority}
                )
        except Exception as e:
            logger.error(f"Policy evaluation error: {e}", exc_info=True)
        return None

class Engine:
    def __init__(self, policies: List[Policy]):
        self.policies = sorted(policies, key=lambda p: p.priority, reverse=True)

    def decide(self, req: Request) -> Decision:
        last: Optional[Decision] = None
        
        for p in self.policies:
            try:
                d = p.eval(req)
                if d is not None:
                    if d.allow:
                        logger.info(f"Access granted: {d.reason} for {req.action}")
                        return d
                    last = d
            except Exception as e:
                logger.error(f"Policy evaluation error: {e}", exc_info=True)
                continue
                
        if last:
            logger.warning(f"Access denied: {last.reason} for {req.action}")
        else:
            logger.warning(f"No policy matched for {req.action}")
            
        return last or Decision(False, "no_policy_matched")
