from typing import Optional
from sqlalchemy.orm import Session
from ideahub_platform.db.models.workspace import Workspace
from ideahub_platform.common.logging import get_logger

logger = get_logger(__name__)

class TenantResolver:
    """Resolves workspace/tenant from URL or subdomain."""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def resolve_from_url(self, url: str) -> Optional[Workspace]:
        """Resolve workspace from URL path."""
        try:
            # Extract workspace identifier from URL
            # Example: /workspace/acme-corp/communities -> acme-corp
            parts = url.strip('/').split('/')
            if len(parts) >= 2 and parts[0] == 'workspace':
                workspace_url = parts[1]
                return self._find_by_url(workspace_url)
            return None
        except Exception as e:
            logger.error(f"Error resolving tenant from URL {url}: {e}")
            return None
    
    def resolve_from_subdomain(self, subdomain: str) -> Optional[Workspace]:
        """Resolve workspace from subdomain."""
        try:
            return self._find_by_url(subdomain)
        except Exception as e:
            logger.error(f"Error resolving tenant from subdomain {subdomain}: {e}")
            return None
    
    def _find_by_url(self, workspace_url: str) -> Optional[Workspace]:
        """Find workspace by URL identifier."""
        try:
            workspace = self.db_session.query(Workspace).filter(
                Workspace.url == workspace_url
            ).first()
            
            if workspace:
                logger.info(f"Resolved workspace: {workspace.name} (ID: {workspace.id})")
            else:
                logger.warning(f"Workspace not found for URL: {workspace_url}")
            
            return workspace
        except Exception as e:
            logger.error(f"Database error finding workspace by URL {workspace_url}: {e}")
            return None

def get_workspace_from_request(request_url: str, db_session: Session) -> Optional[Workspace]:
    """Convenience function to get workspace from request URL."""
    resolver = TenantResolver(db_session)
    return resolver.resolve_from_url(request_url)
