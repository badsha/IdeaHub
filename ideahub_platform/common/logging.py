import logging
import sys
import json
import os
from typing import Any, Dict
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """Structured JSON formatter for production logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
            
        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            payload.update(record.extra_fields)
            
        return json.dumps(payload, ensure_ascii=False)

class StructuredLogger:
    """Enhanced logger with structured logging capabilities."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        
    def _log_with_context(self, level: int, message: str, **kwargs):
        """Log with additional context fields."""
        extra_fields = kwargs.pop("extra_fields", {})
        extra_fields.update(kwargs)
        
        record = self.logger.makeRecord(
            self.logger.name, level, "", 0, message, (), None
        )
        record.extra_fields = extra_fields
        self.logger.handle(record)
        
    def info(self, message: str, **kwargs):
        self._log_with_context(logging.INFO, message, **kwargs)
        
    def warning(self, message: str, **kwargs):
        self._log_with_context(logging.WARNING, message, **kwargs)
        
    def error(self, message: str, **kwargs):
        self._log_with_context(logging.ERROR, message, **kwargs)
        
    def debug(self, message: str, **kwargs):
        self._log_with_context(logging.DEBUG, message, **kwargs)

def configure_logging(level: str = "INFO", log_file: str = None) -> None:
    """Configure logging for production use."""
    
    # Set log level
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create formatter
    formatter = JsonFormatter()
    
    # Create handlers
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=handlers,
        force=True
    )
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    # Log configuration
    logging.info("Logging configured", extra_fields={
        "log_level": level,
        "log_file": log_file,
        "handlers": [h.__class__.__name__ for h in handlers]
    })

def get_logger(name: str) -> StructuredLogger:
    """Get a structured logger instance."""
    return StructuredLogger(name)
