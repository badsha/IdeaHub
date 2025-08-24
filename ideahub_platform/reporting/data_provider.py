from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from ideahub_platform.db.models.workspace import Workspace
from ideahub_platform.db.models.community import Community
from ideahub_platform.db.models.idea import Idea
from ideahub_platform.db.models.member import Member
from ideahub_platform.reporting.models import ActivityLog
from ideahub_platform.common.logging import get_logger

logger = get_logger(__name__)

class ReportingDataProvider:
    """Data provider for reporting queries and aggregations."""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def find_workspace_ids(self, active_only: bool = True) -> List[int]:
        """Get all workspace IDs, optionally filtered by active status."""
        query = self.db_session.query(Workspace.id)
        if active_only:
            # Add any active workspace filters here
            pass
        return [row[0] for row in query.all()]
    
    def find_community_ids(self, workspace_id: Optional[int] = None) -> List[int]:
        """Get community IDs, optionally filtered by workspace."""
        query = self.db_session.query(Community.id)
        if workspace_id:
            query = query.filter(Community.workspace_id == workspace_id)
        return [row[0] for row in query.all()]
    
    def get_idea_statistics(self, workspace_id: int, community_id: Optional[int] = None, 
                          start_date: Optional[datetime] = None, 
                          end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get idea statistics for a workspace/community."""
        query = self.db_session.query(Idea).filter(Idea.community_id.in_(
            self.db_session.query(Community.id).filter(Community.workspace_id == workspace_id)
        ))
        
        if community_id:
            query = query.filter(Idea.community_id == community_id)
        
        if start_date:
            query = query.filter(Idea.created_at >= start_date)
        if end_date:
            query = query.filter(Idea.created_at <= end_date)
        
        ideas = query.all()
        
        stats = {
            'total_ideas': len(ideas),
            'new_ideas': len([i for i in ideas if i.status == 'draft']),
            'implemented_ideas': len([i for i in ideas if i.status == 'implemented']),
            'archived_ideas': len([i for i in ideas if i.status == 'archived']),
            'by_status': {},
            'by_visibility': {},
            'by_community': {}
        }
        
        # Group by status
        for idea in ideas:
            status = idea.status
            stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
            
            visibility = idea.visibility
            stats['by_visibility'][visibility] = stats['by_visibility'].get(visibility, 0) + 1
            
            comm_id = idea.community_id
            stats['by_community'][comm_id] = stats['by_community'].get(comm_id, 0) + 1
        
        return stats
    
    def get_community_statistics(self, workspace_id: int, 
                               start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get community statistics for a workspace."""
        communities = self.db_session.query(Community).filter(
            Community.workspace_id == workspace_id
        ).all()
        
        stats = {
            'total_communities': len(communities),
            'public_communities': len([c for c in communities if c.public]),
            'private_communities': len([c for c in communities if not c.public]),
            'communities_with_ideas': 0,
            'avg_ideas_per_community': 0.0
        }
        
        total_ideas = 0
        for community in communities:
            idea_count = self.db_session.query(Idea).filter(
                Idea.community_id == community.id
            ).count()
            if idea_count > 0:
                stats['communities_with_ideas'] += 1
            total_ideas += idea_count
        
        if stats['total_communities'] > 0:
            stats['avg_ideas_per_community'] = total_ideas / stats['total_communities']
        
        return stats
    
    def get_workspace_statistics(self, workspace_id: int,
                               start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get comprehensive workspace statistics."""
        workspace = self.db_session.query(Workspace).filter(
            Workspace.id == workspace_id
        ).first()
        
        if not workspace:
            return {}
        
        # Get community stats
        community_stats = self.get_community_statistics(workspace_id, start_date, end_date)
        
        # Get idea stats
        idea_stats = self.get_idea_statistics(workspace_id, start_date=start_date, end_date=end_date)
        
        # Get member stats
        member_count = self.db_session.query(Member).join(
            Member.workspaces
        ).filter(Workspace.id == workspace_id).count()
        
        stats = {
            'workspace_id': workspace_id,
            'workspace_name': workspace.name,
            'workspace_url': workspace.url,
            'total_members': member_count,
            'total_communities': community_stats.get('total_communities', 0),
            'total_ideas': idea_stats.get('total_ideas', 0),
            'implementation_rate': 0.0,
            'avg_ideas_per_community': community_stats.get('avg_ideas_per_community', 0.0),
            'avg_members_per_community': 0.0,
            'public_communities': community_stats.get('public_communities', 0),
            'private_communities': community_stats.get('private_communities', 0)
        }
        
        # Calculate implementation rate
        if idea_stats.get('total_ideas', 0) > 0:
            stats['implementation_rate'] = (
                idea_stats.get('implemented_ideas', 0) / idea_stats.get('total_ideas', 0)
            ) * 100
        
        # Calculate average members per community
        if stats['total_communities'] > 0:
            stats['avg_members_per_community'] = stats['total_members'] / stats['total_communities']
        
        return stats
    
    def get_activity_logs(self, workspace_id: int, 
                         activity_type: Optional[str] = None,
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None,
                         limit: int = 1000) -> List[Dict[str, Any]]:
        """Get activity logs for reporting."""
        query = self.db_session.query(ActivityLog).filter(
            ActivityLog.workspace_id == workspace_id
        )
        
        if activity_type:
            query = query.filter(ActivityLog.activity_type == activity_type)
        
        if start_date:
            query = query.filter(ActivityLog.timestamp >= start_date)
        if end_date:
            query = query.filter(ActivityLog.timestamp <= end_date)
        
        query = query.order_by(ActivityLog.timestamp.desc()).limit(limit)
        
        logs = query.all()
        return [
            {
                'id': log.id,
                'activity_type': log.activity_type,
                'entity_type': log.entity_type,
                'entity_id': log.entity_id,
                'community_id': log.community_id,
                'member_id': log.member_id,
                'activity_data': log.activity_data,
                'timestamp': log.timestamp.isoformat(),
                'session_id': log.session_id,
                'ip_address': log.ip_address
            }
            for log in logs
        ]
    
    def get_daily_activity_summary(self, workspace_id: int, 
                                 date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get daily activity summary for a workspace."""
        if not date:
            date = datetime.now().date()
        
        start_date = datetime.combine(date, datetime.min.time())
        end_date = datetime.combine(date, datetime.max.time())
        
        # Get activity logs for the day
        logs = self.get_activity_logs(workspace_id, start_date=start_date, end_date=end_date)
        
        # Group by activity type
        activity_summary = {}
        for log in logs:
            activity_type = log['activity_type']
            if activity_type not in activity_summary:
                activity_summary[activity_type] = 0
            activity_summary[activity_type] += 1
        
        return {
            'date': date.isoformat(),
            'workspace_id': workspace_id,
            'total_activities': len(logs),
            'activity_breakdown': activity_summary,
            'unique_participants': len(set(log['member_id'] for log in logs if log['member_id']))
        }
