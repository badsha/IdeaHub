# Event type definitions
from enum import Enum
from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime

class EventType(Enum):
    """Application event types."""
    # Workspace events
    WORKSPACE_CREATED = "workspace.created"
    WORKSPACE_UPDATED = "workspace.updated"
    WORKSPACE_DELETED = "workspace.deleted"
    
    # Community events
    COMMUNITY_CREATED = "community.created"
    COMMUNITY_UPDATED = "community.updated"
    COMMUNITY_DELETED = "community.deleted"
    
    # Idea events
    IDEA_CREATED = "idea.created"
    IDEA_UPDATED = "idea.updated"
    IDEA_DELETED = "idea.deleted"
    IDEA_VOTED = "idea.voted"
    IDEA_COMMENTED = "idea.commented"
    
    # Member events
    MEMBER_JOINED = "member.joined"
    MEMBER_LEFT = "member.left"
    MEMBER_ROLE_CHANGED = "member.role_changed"
    
    # Campaign events
    CAMPAIGN_CREATED = "campaign.created"
    CAMPAIGN_UPDATED = "campaign.updated"
    CAMPAIGN_DELETED = "campaign.deleted"
    CAMPAIGN_STARTED = "campaign.started"
    CAMPAIGN_ENDED = "campaign.ended"

@dataclass
class EventMetadata:
    """Event metadata for tracking and auditing."""
    event_id: str
    correlation_id: str
    user_id: str
    timestamp: datetime
    source: str = "ideahub-api"
    version: str = "1.0"

@dataclass
class BaseEvent:
    """Base event structure."""
    event_type: EventType
    data: Dict[str, Any]
    metadata: EventMetadata

# Event data schemas
@dataclass
class WorkspaceEventData:
    """Workspace event data."""
    workspace_id: int
    workspace_name: str
    owner_id: int
    public_default: bool

@dataclass
class CommunityEventData:
    """Community event data."""
    community_id: int
    workspace_id: int
    community_name: str
    public: bool

@dataclass
class IdeaEventData:
    """Idea event data."""
    idea_id: int
    community_id: int
    author_id: int
    title: str
    visibility: str

@dataclass
class MemberEventData:
    """Member event data."""
    member_id: int
    workspace_id: int
    role: str
    joined_at: datetime
