from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ideahub_platform.reporting.data_provider import ReportingDataProvider
from ideahub_platform.reporting.services import ReportingService
from ideahub_platform.common.logging import get_logger

logger = get_logger(__name__)

class ProcessorBase:
    """Base class for reporting processors."""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.data_provider = ReportingDataProvider(db_session)
        self.reporting_service = ReportingService(db_session)
    
    def process_workspace(self, workspace_id: int, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Process a single workspace for the given date range."""
        raise NotImplementedError
    
    def process_all_workspaces(self, start_date: Optional[datetime] = None, 
                             end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Process all workspaces for the given date range."""
        if not start_date:
            start_date = datetime.now() - timedelta(days=1)
        if not end_date:
            end_date = datetime.now()
        
        workspace_ids = self.data_provider.find_workspace_ids()
        results = {
            'processed_workspaces': 0,
            'errors': [],
            'start_date': start_date,
            'end_date': end_date
        }
        
        for workspace_id in workspace_ids:
            try:
                self.process_workspace(workspace_id, start_date, end_date)
                results['processed_workspaces'] += 1
                logger.info(f"Processed workspace {workspace_id}")
            except Exception as e:
                error_msg = f"Error processing workspace {workspace_id}: {e}"
                results['errors'].append(error_msg)
                logger.error(error_msg)
        
        return results


class IdeaStatProcessor(ProcessorBase):
    """Processor for idea statistics."""
    
    def process_workspace(self, workspace_id: int, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Process idea statistics for a workspace."""
        community_ids = self.data_provider.find_community_ids(workspace_id)
        results = {}
        
        for community_id in community_ids:
            try:
                # Get idea statistics for this community
                idea_stats = self.data_provider.get_idea_statistics(
                    workspace_id, community_id, start_date, end_date
                )
                
                # Save statistics for each day in the range
                current_date = start_date.date()
                end_date_obj = end_date.date()
                
                while current_date <= end_date_obj:
                    date_obj = datetime.combine(current_date, datetime.min.time())
                    
                    # Calculate daily stats
                    daily_stats = self._calculate_daily_idea_stats(
                        workspace_id, community_id, date_obj, idea_stats
                    )
                    
                    # Save to database
                    self.reporting_service.save_idea_statistics(
                        workspace_id, community_id, date_obj, daily_stats
                    )
                    
                    current_date += timedelta(days=1)
                
                results[community_id] = idea_stats
                logger.info(f"Processed idea statistics for workspace {workspace_id}, community {community_id}")
                
            except Exception as e:
                logger.error(f"Error processing idea statistics for community {community_id}: {e}")
                raise
        
        return results
    
    def _calculate_daily_idea_stats(self, workspace_id: int, community_id: int, 
                                  date: datetime, overall_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate daily idea statistics."""
        # For now, distribute overall stats evenly across days
        # In a real implementation, you'd calculate actual daily metrics
        
        days_in_period = 1  # For daily processing
        
        return {
            'total_ideas': overall_stats.get('total_ideas', 0),
            'new_ideas': overall_stats.get('new_ideas', 0) // days_in_period,
            'implemented_ideas': overall_stats.get('implemented_ideas', 0),
            'archived_ideas': overall_stats.get('archived_ideas', 0),
            'metadata': {
                'calculation_date': date.isoformat(),
                'workspace_id': workspace_id,
                'community_id': community_id
            }
        }
    
    def reset(self, workspace_id: int, start_date: datetime) -> Dict[str, Any]:
        """Reset and recompute idea statistics from a start date."""
        logger.info(f"Resetting idea statistics for workspace {workspace_id} from {start_date}")
        
        # Delete existing statistics from start_date onwards
        # This would be implemented with actual database deletion
        
        # Recompute from start_date to now
        end_date = datetime.now()
        return self.process_workspace(workspace_id, start_date, end_date)


class CommunityStatProcessor(ProcessorBase):
    """Processor for community statistics."""
    
    def process_workspace(self, workspace_id: int, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Process community statistics for a workspace."""
        try:
            # Get community statistics
            community_stats = self.data_provider.get_community_statistics(
                workspace_id, start_date, end_date
            )
            
            # Save statistics for each day in the range
            current_date = start_date.date()
            end_date_obj = end_date.date()
            
            while current_date <= end_date_obj:
                date_obj = datetime.combine(current_date, datetime.min.time())
                
                # Calculate daily stats
                daily_stats = self._calculate_daily_community_stats(
                    workspace_id, date_obj, community_stats
                )
                
                # Save to database (for each community)
                community_ids = self.data_provider.find_community_ids(workspace_id)
                for community_id in community_ids:
                    self.reporting_service.save_community_statistics(
                        workspace_id, community_id, date_obj, daily_stats
                    )
                
                current_date += timedelta(days=1)
            
            logger.info(f"Processed community statistics for workspace {workspace_id}")
            return community_stats
            
        except Exception as e:
            logger.error(f"Error processing community statistics for workspace {workspace_id}: {e}")
            raise
    
    def _calculate_daily_community_stats(self, workspace_id: int, date: datetime,
                                       overall_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate daily community statistics."""
        return {
            'total_members': overall_stats.get('total_members', 0),
            'active_members': overall_stats.get('active_members', 0),
            'new_members': overall_stats.get('new_members', 0),
            'total_ideas': overall_stats.get('total_ideas', 0),
            'total_campaigns': overall_stats.get('total_campaigns', 0),
            'total_activities': overall_stats.get('total_activities', 0),
            'avg_ideas_per_member': overall_stats.get('avg_ideas_per_member', 0.0),
            'avg_votes_per_idea': overall_stats.get('avg_votes_per_idea', 0.0),
            'avg_comments_per_idea': overall_stats.get('avg_comments_per_idea', 0.0),
            'metadata': {
                'calculation_date': date.isoformat(),
                'workspace_id': workspace_id
            }
        }


class WorkspaceStatProcessor(ProcessorBase):
    """Processor for workspace statistics."""
    
    def process_workspace(self, workspace_id: int, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Process workspace statistics."""
        try:
            # Get workspace statistics
            workspace_stats = self.data_provider.get_workspace_statistics(
                workspace_id, start_date, end_date
            )
            
            # Save statistics for each day in the range
            current_date = start_date.date()
            end_date_obj = end_date.date()
            
            while current_date <= end_date_obj:
                date_obj = datetime.combine(current_date, datetime.min.time())
                
                # Calculate daily stats
                daily_stats = self._calculate_daily_workspace_stats(
                    workspace_id, date_obj, workspace_stats
                )
                
                # Save to database
                self.reporting_service.save_workspace_statistics(
                    workspace_id, date_obj, daily_stats
                )
                
                current_date += timedelta(days=1)
            
            logger.info(f"Processed workspace statistics for workspace {workspace_id}")
            return workspace_stats
            
        except Exception as e:
            logger.error(f"Error processing workspace statistics for workspace {workspace_id}: {e}")
            raise
    
    def _calculate_daily_workspace_stats(self, workspace_id: int, date: datetime,
                                       overall_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate daily workspace statistics."""
        return {
            'total_communities': overall_stats.get('total_communities', 0),
            'total_members': overall_stats.get('total_members', 0),
            'total_ideas': overall_stats.get('total_ideas', 0),
            'total_campaigns': overall_stats.get('total_campaigns', 0),
            'active_communities': overall_stats.get('active_communities', 0),
            'active_members': overall_stats.get('active_members', 0),
            'new_ideas_today': overall_stats.get('new_ideas_today', 0),
            'avg_ideas_per_community': overall_stats.get('avg_ideas_per_community', 0.0),
            'avg_members_per_community': overall_stats.get('avg_members_per_community', 0.0),
            'implementation_rate': overall_stats.get('implementation_rate', 0.0),
            'metadata': {
                'calculation_date': date.isoformat(),
                'workspace_id': workspace_id
            }
        }
