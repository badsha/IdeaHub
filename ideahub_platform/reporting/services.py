from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ideahub_platform.reporting.models import (
    IdeaStatistics, CommunityStatistics, WorkspaceStatistics, ActivityLog
)
from ideahub_platform.reporting.data_provider import ReportingDataProvider
from ideahub_platform.common.logging import get_logger

logger = get_logger(__name__)

class ReportingService:
    """Service for managing reporting statistics and metrics."""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.data_provider = ReportingDataProvider(db_session)
    
    def save_idea_statistics(self, workspace_id: int, community_id: int, 
                           date: datetime, stats: Dict[str, Any]) -> IdeaStatistics:
        """Save idea statistics for a specific date."""
        try:
            existing = self.db_session.query(IdeaStatistics).filter(
                IdeaStatistics.workspace_id == workspace_id,
                IdeaStatistics.community_id == community_id,
                IdeaStatistics.date == date
            ).first()
            
            if existing:
                existing.total_ideas = stats.get('total_ideas', 0)
                existing.new_ideas = stats.get('new_ideas', 0)
                existing.implemented_ideas = stats.get('implemented_ideas', 0)
                existing.archived_ideas = stats.get('archived_ideas', 0)
                existing.metadata = stats.get('metadata', {})
                existing.updated_at = datetime.utcnow()
                self.db_session.commit()
                return existing
            else:
                idea_stats = IdeaStatistics(
                    workspace_id=workspace_id,
                    community_id=community_id,
                    date=date,
                    total_ideas=stats.get('total_ideas', 0),
                    new_ideas=stats.get('new_ideas', 0),
                    implemented_ideas=stats.get('implemented_ideas', 0),
                    archived_ideas=stats.get('archived_ideas', 0),
                    metadata=stats.get('metadata', {})
                )
                self.db_session.add(idea_stats)
                self.db_session.commit()
                return idea_stats
                
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error saving idea statistics: {e}")
            raise
    
    def save_community_statistics(self, workspace_id: int, community_id: int,
                                date: datetime, stats: Dict[str, Any]) -> CommunityStatistics:
        """Save community statistics for a specific date."""
        try:
            # Check if statistics already exist for this date
            existing = self.db_session.query(CommunityStatistics).filter(
                CommunityStatistics.workspace_id == workspace_id,
                CommunityStatistics.community_id == community_id,
                CommunityStatistics.date == date
            ).first()
            
            if existing:
                # Update existing record
                existing.total_members = stats.get('total_members', 0)
                existing.active_members = stats.get('active_members', 0)
                existing.new_members = stats.get('new_members', 0)
                existing.total_ideas = stats.get('total_ideas', 0)
                existing.total_campaigns = stats.get('total_campaigns', 0)
                existing.total_activities = stats.get('total_activities', 0)
                existing.avg_ideas_per_member = stats.get('avg_ideas_per_member', 0.0)
                existing.avg_votes_per_idea = stats.get('avg_votes_per_idea', 0.0)
                existing.avg_comments_per_idea = stats.get('avg_comments_per_idea', 0.0)
                existing.metadata = stats.get('metadata', {})
                existing.updated_at = datetime.utcnow()
                
                self.db_session.commit()
                logger.info(f"Updated community statistics for workspace {workspace_id}, community {community_id}, date {date}")
                return existing
            else:
                # Create new record
                community_stats = CommunityStatistics(
                    workspace_id=workspace_id,
                    community_id=community_id,
                    date=date,
                    total_members=stats.get('total_members', 0),
                    active_members=stats.get('active_members', 0),
                    new_members=stats.get('new_members', 0),
                    total_ideas=stats.get('total_ideas', 0),
                    total_campaigns=stats.get('total_campaigns', 0),
                    total_activities=stats.get('total_activities', 0),
                    avg_ideas_per_member=stats.get('avg_ideas_per_member', 0.0),
                    avg_votes_per_idea=stats.get('avg_votes_per_idea', 0.0),
                    avg_comments_per_idea=stats.get('avg_comments_per_idea', 0.0),
                    metadata=stats.get('metadata', {})
                )
                
                self.db_session.add(community_stats)
                self.db_session.commit()
                logger.info(f"Created community statistics for workspace {workspace_id}, community {community_id}, date {date}")
                return community_stats
                
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error saving community statistics: {e}")
            raise
    
    def save_workspace_statistics(self, workspace_id: int, date: datetime,
                                stats: Dict[str, Any]) -> WorkspaceStatistics:
        """Save workspace statistics for a specific date."""
        try:
            # Check if statistics already exist for this date
            existing = self.db_session.query(WorkspaceStatistics).filter(
                WorkspaceStatistics.workspace_id == workspace_id,
                WorkspaceStatistics.date == date
            ).first()
            
            if existing:
                # Update existing record
                existing.total_communities = stats.get('total_communities', 0)
                existing.total_members = stats.get('total_members', 0)
                existing.total_ideas = stats.get('total_ideas', 0)
                existing.total_campaigns = stats.get('total_campaigns', 0)
                existing.active_communities = stats.get('active_communities', 0)
                existing.active_members = stats.get('active_members', 0)
                existing.new_ideas_today = stats.get('new_ideas_today', 0)
                existing.avg_ideas_per_community = stats.get('avg_ideas_per_community', 0.0)
                existing.avg_members_per_community = stats.get('avg_members_per_community', 0.0)
                existing.implementation_rate = stats.get('implementation_rate', 0.0)
                existing.metadata = stats.get('metadata', {})
                existing.updated_at = datetime.utcnow()
                
                self.db_session.commit()
                logger.info(f"Updated workspace statistics for workspace {workspace_id}, date {date}")
                return existing
            else:
                # Create new record
                workspace_stats = WorkspaceStatistics(
                    workspace_id=workspace_id,
                    date=date,
                    total_communities=stats.get('total_communities', 0),
                    total_members=stats.get('total_members', 0),
                    total_ideas=stats.get('total_ideas', 0),
                    total_campaigns=stats.get('total_campaigns', 0),
                    active_communities=stats.get('active_communities', 0),
                    active_members=stats.get('active_members', 0),
                    new_ideas_today=stats.get('new_ideas_today', 0),
                    avg_ideas_per_community=stats.get('avg_ideas_per_community', 0.0),
                    avg_members_per_community=stats.get('avg_members_per_community', 0.0),
                    implementation_rate=stats.get('implementation_rate', 0.0),
                    metadata=stats.get('metadata', {})
                )
                
                self.db_session.add(workspace_stats)
                self.db_session.commit()
                logger.info(f"Created workspace statistics for workspace {workspace_id}, date {date}")
                return workspace_stats
                
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error saving workspace statistics: {e}")
            raise
    
    def log_activity(self, workspace_id: int, activity_type: str, entity_type: str,
                    entity_id: Optional[int] = None, community_id: Optional[int] = None,
                    member_id: Optional[int] = None, activity_data: Optional[Dict[str, Any]] = None) -> ActivityLog:
        """Log an activity for reporting purposes."""
        try:
            activity_log = ActivityLog(
                workspace_id=workspace_id,
                community_id=community_id,
                member_id=member_id,
                activity_type=activity_type,
                entity_type=entity_type,
                entity_id=entity_id,
                activity_data=activity_data or {}
            )
            
            self.db_session.add(activity_log)
            self.db_session.commit()
            return activity_log
            
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error logging activity: {e}")
            raise
    
    def get_statistics_summary(self, workspace_id: int, 
                             start_date: Optional[datetime] = None,
                             end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get a comprehensive statistics summary for a workspace."""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        workspace_stats = self.data_provider.get_workspace_statistics(
            workspace_id, start_date, end_date
        )
        
        activity_summary = self.data_provider.get_daily_activity_summary(workspace_id)
        
        return {
            'workspace': workspace_stats,
            'activity_summary': activity_summary,
            'date_range': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
        }
