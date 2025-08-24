from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
import os
import logging
from typing import Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# Database configuration - PostgreSQL for all environments
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# PostgreSQL configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:password@localhost:5432/ideahub")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "20"))
DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "3600"))
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"

# Create engine with production-ready PostgreSQL configuration
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
    pool_timeout=DB_POOL_TIMEOUT,
    pool_recycle=DB_POOL_RECYCLE,
    pool_pre_ping=True,
    echo=DB_ECHO,
    # PostgreSQL-specific optimizations
    connect_args={
        "application_name": f"ideahub-{ENVIRONMENT}",
        "options": "-c timezone=utc"
    }
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

class DatabaseManager:
    """Database connection and health check manager."""
    
    def __init__(self):
        self.engine = engine
        self.session_factory = SessionLocal
        
    def get_session(self):
        """Get a database session."""
        return self.session_factory()
        
    @contextmanager
    def get_db_session(self):
        """Context manager for database sessions."""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}", exc_info=True)
            raise
        finally:
            session.close()
            
    async def health_check(self) -> bool:
        """Check database connectivity."""
        try:
            with self.get_db_session() as session:
                result = session.execute(text("SELECT 1"))
                return result.scalar() == 1
        except SQLAlchemyError as e:
            logger.error(f"Database health check failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error in health check: {e}")
            return False
            
    def get_connection_info(self) -> dict:
        """Get database connection information."""
        # Hide password in connection info
        safe_url = DATABASE_URL
        if "@" in DATABASE_URL:
            parts = DATABASE_URL.split("@")
            if ":" in parts[0]:
                protocol_user = parts[0].split(":")
                if len(protocol_user) >= 3:
                    safe_url = f"{protocol_user[0]}:{protocol_user[1]}:***@{parts[1]}"
        
        return {
            "url": safe_url,
            "environment": ENVIRONMENT,
            "pool_size": DB_POOL_SIZE,
            "max_overflow": DB_MAX_OVERFLOW,
            "pool_timeout": DB_POOL_TIMEOUT,
            "pool_recycle": DB_POOL_RECYCLE,
            "echo": DB_ECHO
        }
        
    def create_tables(self):
        """Create all tables (for development/testing)."""
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}", exc_info=True)
            raise

# Global database manager instance
db_manager = DatabaseManager()

def get_db():
    """Dependency to get database session."""
    with db_manager.get_db_session() as session:
        yield session
