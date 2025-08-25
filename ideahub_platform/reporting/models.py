from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ideahub_platform.db.base import Base
from datetime import datetime
from typing import Dict, Any


class IdeaStatistics(Base):
    __tablename__ = "idea_statistics"
    __table_args__ = {'schema': 'reporting'}

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, nullable=False, index=True)
    community_id = Column(Integer, nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    
    # Metrics
    total_ideas = Column(Integer, default=0)
    new_ideas = Column(Integer, default=0)
    implemented_ideas = Column(Integer, default=0)
    archived_ideas = Column(Integer, default=0)
    
    # Engagement metrics
    total_votes = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    unique_participants = Column(Integer, default=0)
    
    # Performance metrics
    avg_implementation_time_days = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)  # implemented / total
    
    # Metadata
    extra_data = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class CommunityStatistics(Base):
    __tablename__ = "community_statistics"
    __table_args__ = {'schema': 'reporting'}

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, nullable=False, index=True)
    community_id = Column(Integer, nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    
    # Community metrics
    total_members = Column(Integer, default=0)
    active_members = Column(Integer, default=0)
    new_members = Column(Integer, default=0)
    
    # Activity metrics
    total_ideas = Column(Integer, default=0)
    total_campaigns = Column(Integer, default=0)
    total_activities = Column(Integer, default=0)
    
    # Engagement metrics
    avg_ideas_per_member = Column(Float, default=0.0)
    avg_votes_per_idea = Column(Float, default=0.0)
    avg_comments_per_idea = Column(Float, default=0.0)
    
    # Metadata
    extra_data = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class WorkspaceStatistics(Base):
    __tablename__ = "workspace_statistics"
    __table_args__ = {'schema': 'reporting'}

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    
    # Workspace metrics
    total_communities = Column(Integer, default=0)
    total_members = Column(Integer, default=0)
    total_ideas = Column(Integer, default=0)
    total_campaigns = Column(Integer, default=0)
    
    # Activity metrics
    active_communities = Column(Integer, default=0)
    active_members = Column(Integer, default=0)
    new_ideas_today = Column(Integer, default=0)
    
    # Performance metrics
    avg_ideas_per_community = Column(Float, default=0.0)
    avg_members_per_community = Column(Float, default=0.0)
    implementation_rate = Column(Float, default=0.0)
    
    # Metadata
    extra_data = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    __table_args__ = {'schema': 'reporting'}

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, nullable=False, index=True)
    community_id = Column(Integer, nullable=True, index=True)
    member_id = Column(Integer, nullable=True, index=True)
    
    # Activity details
    activity_type = Column(String(100), nullable=False, index=True)  # idea_created, idea_voted, etc.
    entity_type = Column(String(50), nullable=False)  # idea, community, member, etc.
    entity_id = Column(Integer, nullable=True)
    
    # Activity data
    activity_data = Column(JSON, default=dict)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Metadata
    session_id = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
