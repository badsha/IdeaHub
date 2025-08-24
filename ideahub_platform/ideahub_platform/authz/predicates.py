# Simple starter predicates

def is_authenticated(req):
    return bool(getattr(req.subject, "is_authenticated", False))
