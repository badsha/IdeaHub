from ideahub_platform.authz.engine import Engine, Policy, Request, Decision
from ideahub_platform.authz.predicates import is_authenticated, is_admin, action_matches

def test_allow_policy():
    """Test that an allow policy works correctly."""
    policy = Policy("allow", [lambda r: True], reason="test_allow")
    req = Request(subject=None, action="TEST", resource=None, ctx={})
    decision = policy.eval(req)
    assert decision is not None
    assert decision.allow is True
    assert decision.reason == "test_allow"

def test_deny_policy():
    """Test that a deny policy works correctly."""
    policy = Policy("deny", [lambda r: True], reason="test_deny")
    req = Request(subject=None, action="TEST", resource=None, ctx={})
    decision = policy.eval(req)
    assert decision is not None
    assert decision.allow is False
    assert decision.reason == "test_deny"

def test_policy_no_match():
    """Test that a policy with false predicate returns None."""
    policy = Policy("allow", [lambda r: False], reason="test_no_match")
    req = Request(subject=None, action="TEST", resource=None, ctx={})
    decision = policy.eval(req)
    assert decision is None

def test_engine_decision():
    """Test that the engine returns the correct decision."""
    policies = [
        Policy("allow", [lambda r: r.action == "ALLOW"], reason="allow_action"),
        Policy("deny", [lambda r: r.action == "DENY"], reason="deny_action"),
    ]
    engine = Engine(policies)
    
    # Test allow
    req = Request(subject=None, action="ALLOW", resource=None, ctx={})
    decision = engine.decide(req)
    assert decision.allow is True
    assert decision.reason == "allow_action"
    
    # Test deny
    req = Request(subject=None, action="DENY", resource=None, ctx={})
    decision = engine.decide(req)
    assert decision.allow is False
    assert decision.reason == "deny_action"
    
    # Test no match
    req = Request(subject=None, action="UNKNOWN", resource=None, ctx={})
    decision = engine.decide(req)
    assert decision.allow is False
    assert decision.reason == "no_policy_matched"

def test_authenticated_predicate():
    """Test the is_authenticated predicate."""
    # Test authenticated subject
    subject = type('Subject', (), {'is_authenticated': True})()
    req = Request(subject=subject, action="TEST", resource=None, ctx={})
    assert is_authenticated(req) is True
    
    # Test unauthenticated subject
    subject = type('Subject', (), {'is_authenticated': False})()
    req = Request(subject=subject, action="TEST", resource=None, ctx={})
    assert is_authenticated(req) is False

def test_admin_predicate():
    """Test the is_admin predicate."""
    # Test admin subject
    subject = type('Subject', (), {'is_admin': True})()
    req = Request(subject=subject, action="TEST", resource=None, ctx={})
    assert is_admin(req) is True
    
    # Test non-admin subject
    subject = type('Subject', (), {'is_admin': False})()
    req = Request(subject=subject, action="TEST", resource=None, ctx={})
    assert is_admin(req) is False

def test_action_matches_predicate():
    """Test the action_matches predicate."""
    req = Request(subject=None, action="TEST_ACTION", resource=None, ctx={})
    assert action_matches(req, "TEST_ACTION") is True
    assert action_matches(req, "OTHER_ACTION") is False
