from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from ideahub_platform.db.base import get_db
from ideahub_platform.reporting.services import ReportingService
from ideahub_platform.reporting.processors import (
    IdeaStatProcessor, CommunityStatProcessor, WorkspaceStatProcessor
)
from ideahub_platform.common.tenant import get_workspace_from_request
from ideahub_platform.common.logging import get_logger
from ideahub_platform.i18n import get_text

logger = get_logger(__name__)

router = APIRouter(prefix="/reporting", tags=["reporting"])

def get_reporting_service(db: Session = Depends(get_db)) -> ReportingService:
    return ReportingService(db)

@router.get("/workspace/{workspace_id}/statistics")
async def get_workspace_statistics(
    workspace_id: int,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get comprehensive workspace statistics."""
    try:
        reporting_service = ReportingService(db)
        
        # Parse dates
        start_dt = None
        end_dt = None
        
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Get statistics summary
        summary = reporting_service.get_statistics_summary(workspace_id, start_dt, end_dt)
        
        return {
            "success": True,
            "data": summary,
            "workspace_id": workspace_id
        }
        
    except Exception as e:
        logger.error(f"Error getting workspace statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve workspace statistics")

@router.get("/workspace/{workspace_id}/activity")
async def get_workspace_activity(
    workspace_id: int,
    activity_type: Optional[str] = Query(None, description="Filter by activity type"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, description="Number of activities to return"),
    db: Session = Depends(get_db)
):
    """Get workspace activity logs."""
    try:
        from ideahub_platform.reporting.data_provider import ReportingDataProvider
        data_provider = ReportingDataProvider(db)
        
        # Parse dates
        start_dt = None
        end_dt = None
        
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Get activity logs
        activities = data_provider.get_activity_logs(
            workspace_id, activity_type, start_dt, end_dt, limit
        )
        
        return {
            "success": True,
            "data": activities,
            "workspace_id": workspace_id,
            "total_count": len(activities)
        }
        
    except Exception as e:
        logger.error(f"Error getting workspace activity: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve workspace activity")

@router.get("/workspace/{workspace_id}/daily-summary")
async def get_daily_activity_summary(
    workspace_id: int,
    date: Optional[str] = Query(None, description="Date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get daily activity summary for a workspace."""
    try:
        from ideahub_platform.reporting.data_provider import ReportingDataProvider
        data_provider = ReportingDataProvider(db)
        
        # Parse date
        target_date = None
        if date:
            target_date = datetime.strptime(date, "%Y-%m-%d")
        
        # Get daily summary
        summary = data_provider.get_daily_activity_summary(workspace_id, target_date)
        
        return {
            "success": True,
            "data": summary,
            "workspace_id": workspace_id
        }
        
    except Exception as e:
        logger.error(f"Error getting daily activity summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve daily activity summary")

@router.post("/workspace/{workspace_id}/process-statistics")
async def process_workspace_statistics(
    workspace_id: int,
    processor_type: str = Query(..., description="Type of processor: idea, community, workspace, all"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Process and compute statistics for a workspace."""
    try:
        # Parse dates
        start_dt = None
        end_dt = None
        
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        results = {}
        
        if processor_type in ["idea", "all"]:
            idea_processor = IdeaStatProcessor(db)
            results["idea"] = idea_processor.process_workspace(workspace_id, start_dt, end_dt)
        
        if processor_type in ["community", "all"]:
            community_processor = CommunityStatProcessor(db)
            results["community"] = community_processor.process_workspace(workspace_id, start_dt, end_dt)
        
        if processor_type in ["workspace", "all"]:
            workspace_processor = WorkspaceStatProcessor(db)
            results["workspace"] = workspace_processor.process_workspace(workspace_id, start_dt, end_dt)
        
        return {
            "success": True,
            "message": f"Successfully processed {processor_type} statistics",
            "workspace_id": workspace_id,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error processing workspace statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to process workspace statistics")

@router.post("/workspace/{workspace_id}/reset-statistics")
async def reset_workspace_statistics(
    workspace_id: int,
    start_date: str = Query(..., description="Start date (YYYY-MM-DD) for reset"),
    processor_type: str = Query("idea", description="Type of processor to reset"),
    db: Session = Depends(get_db)
):
    """Reset and recompute statistics from a specific date."""
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        
        if processor_type == "idea":
            idea_processor = IdeaStatProcessor(db)
            results = idea_processor.reset(workspace_id, start_dt)
        else:
            raise HTTPException(status_code=400, detail="Only idea processor reset is currently supported")
        
        return {
            "success": True,
            "message": f"Successfully reset {processor_type} statistics from {start_date}",
            "workspace_id": workspace_id,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error resetting workspace statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to reset workspace statistics")

@router.get("/analytics/dashboard")
async def get_analytics_dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get analytics dashboard data for the current workspace."""
    try:
        # Extract workspace from request URL
        workspace = get_workspace_from_request(str(request.url), db)
        
        if not workspace:
            raise HTTPException(status_code=404, detail="Workspace not found")
        
        reporting_service = ReportingService(db)
        
        # Get last 30 days of statistics
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        summary = reporting_service.get_statistics_summary(
            workspace.id, start_date, end_date
        )
        
        # Get recent activity
        from ideahub_platform.reporting.data_provider import ReportingDataProvider
        data_provider = ReportingDataProvider(db)
        recent_activities = data_provider.get_activity_logs(
            workspace.id, limit=50
        )
        
        dashboard_data = {
            "workspace": {
                "id": workspace.id,
                "name": workspace.name,
                "url": workspace.url
            },
            "statistics": summary,
            "recent_activities": recent_activities,
            "last_updated": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "data": dashboard_data
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics dashboard: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics dashboard")

@router.post("/activity/log")
async def log_activity(
    workspace_id: int,
    activity_type: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    community_id: Optional[int] = None,
    member_id: Optional[int] = None,
    activity_data: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db)
):
    """Log an activity for reporting purposes."""
    try:
        reporting_service = ReportingService(db)
        
        activity_log = reporting_service.log_activity(
            workspace_id=workspace_id,
            activity_type=activity_type,
            entity_type=entity_type,
            entity_id=entity_id,
            community_id=community_id,
            member_id=member_id,
            activity_data=activity_data
        )
        
        return {
            "success": True,
            "message": "Activity logged successfully",
            "activity_id": activity_log.id
        }
        
    except Exception as e:
        logger.error(f"Error logging activity: {e}")
        raise HTTPException(status_code=500, detail="Failed to log activity")
