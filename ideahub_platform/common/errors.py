# Production-ready error handling
from typing import Any, Dict, Optional
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class IdeaHubError(Exception):
    """Base exception for IdeaHub application."""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details
        }

class AuthenticationError(IdeaHubError):
    """Authentication related errors."""
    pass

class AuthorizationError(IdeaHubError):
    """Authorization related errors."""
    pass

class ValidationError(IdeaHubError):
    """Data validation errors."""
    pass

class NotFoundError(IdeaHubError):
    """Resource not found errors."""
    pass

class ConflictError(IdeaHubError):
    """Resource conflict errors."""
    pass

class DatabaseError(IdeaHubError):
    """Database related errors."""
    pass

class ExternalServiceError(IdeaHubError):
    """External service integration errors."""
    pass

def handle_exception(exc: Exception) -> HTTPException:
    """Convert internal exceptions to HTTP exceptions."""
    
    if isinstance(exc, IdeaHubError):
        logger.warning(f"Application error: {exc.error_code}", extra_fields={
            "error_code": exc.error_code,
            "details": exc.details
        })
        
        # Map error types to HTTP status codes
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
            
        return HTTPException(
            status_code=status_code,
            detail=exc.to_dict()
        )
    
    # Handle unexpected exceptions
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return HTTPException(
        status_code=500,
        detail={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "details": {}
        }
    )

def log_request_error(request_id: str, error: Exception, context: Dict[str, Any] = None):
    """Log request errors with context."""
    logger.error(f"Request error: {str(error)}", extra_fields={
        "request_id": request_id,
        "error_type": error.__class__.__name__,
        "context": context or {}
    }, exc_info=True)
