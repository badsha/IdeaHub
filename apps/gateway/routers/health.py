from fastapi import APIRouter, Request, Header
from ideahub_platform.db.base import db_manager
from ideahub_platform.common.logging import get_logger
from ideahub_platform.i18n import get_text
from datetime import datetime
import psutil
import os
from typing import Optional

logger = get_logger(__name__)

router = APIRouter()

@router.get("/health")
async def health(accept_language: Optional[str] = Header(None)):
    """Basic health check endpoint."""
    locale = accept_language.split(',')[0].split('-')[0] if accept_language else 'en'
    return {
        "status": "ok", 
        "timestamp": datetime.utcnow().isoformat(),
        "message": get_text("common.loading", locale=locale)
    }

@router.get("/health/detailed")
async def detailed_health(request: Request):
    """Detailed health check with system metrics."""
    
    # Database health check
    db_healthy = await db_manager.health_check()
    
    # System metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Application metrics
    process = psutil.Process(os.getpid())
    
    health_data = {
        "status": "healthy" if db_healthy else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": getattr(request.state, "request_id", "unknown"),
        "checks": {
            "database": {
                "status": "healthy" if db_healthy else "unhealthy",
                "connection_info": db_manager.get_connection_info()
            },
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available": memory.available,
                "disk_percent": disk.percent,
                "disk_free": disk.free
            },
            "application": {
                "process_id": process.pid,
                "memory_usage": process.memory_info().rss,
                "cpu_percent": process.cpu_percent(),
                "threads": process.num_threads()
            }
        }
    }
    
    logger.info("Detailed health check", extra_fields={
        "request_id": getattr(request.state, "request_id", "unknown"),
        "db_healthy": db_healthy,
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent
    })
    
    return health_data

@router.get("/health/ready")
async def readiness_check():
    """Readiness check for Kubernetes."""
    db_healthy = await db_manager.health_check()
    
    if db_healthy:
        return {"status": "ready"}
    else:
        return {"status": "not_ready", "reason": "database_unavailable"}
