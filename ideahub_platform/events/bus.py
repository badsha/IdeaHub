# Production-ready event bus
import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class EventType(Enum):
    """Event types for the application."""
    WORKSPACE_CREATED = "workspace.created"
    WORKSPACE_UPDATED = "workspace.updated"
    WORKSPACE_DELETED = "workspace.deleted"
    COMMUNITY_CREATED = "community.created"
    COMMUNITY_UPDATED = "community.updated"
    COMMUNITY_DELETED = "community.deleted"
    IDEA_CREATED = "idea.created"
    IDEA_UPDATED = "idea.updated"
    IDEA_DELETED = "idea.deleted"
    MEMBER_JOINED = "member.joined"
    MEMBER_LEFT = "member.left"

@dataclass
class Event:
    """Domain event structure."""
    event_type: EventType
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    event_id: Optional[str] = None
    correlation_id: Optional[str] = None
    user_id: Optional[str] = None

class EventBus:
    """Production-ready event bus with async support."""
    
    def __init__(self):
        self._handlers: Dict[EventType, List[Callable]] = {}
        self._middleware: List[Callable] = []
        self._queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        
    def subscribe(self, event_type: EventType, handler: Callable) -> None:
        """Subscribe to an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        logger.info(f"Handler subscribed to {event_type.value}")
        
    def unsubscribe(self, event_type: EventType, handler: Callable) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
                logger.info(f"Handler unsubscribed from {event_type.value}")
            except ValueError:
                logger.warning(f"Handler not found for {event_type.value}")
                
    def add_middleware(self, middleware: Callable) -> None:
        """Add middleware to the event bus."""
        self._middleware.append(middleware)
        logger.info("Middleware added to event bus")
        
    async def publish(self, event: Event) -> None:
        """Publish an event asynchronously."""
        try:
            # Apply middleware
            for middleware in self._middleware:
                event = await middleware(event)
                
            # Add to queue for processing
            await self._queue.put(event)
            logger.info(f"Event published: {event.event_type.value}")
            
        except Exception as e:
            logger.error(f"Error publishing event: {e}", exc_info=True)
            
    def publish_sync(self, event: Event) -> None:
        """Publish an event synchronously."""
        try:
            if event.event_type in self._handlers:
                for handler in self._handlers[event.event_type]:
                    try:
                        handler(event)
                    except Exception as e:
                        logger.error(f"Handler error for {event.event_type.value}: {e}", exc_info=True)
                        
            logger.info(f"Event published synchronously: {event.event_type.value}")
            
        except Exception as e:
            logger.error(f"Error publishing event synchronously: {e}", exc_info=True)
            
    async def start(self) -> None:
        """Start the event bus processing."""
        self._running = True
        logger.info("Event bus started")
        
        while self._running:
            try:
                event = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                await self._process_event(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error in event bus processing: {e}", exc_info=True)
                
    async def stop(self) -> None:
        """Stop the event bus processing."""
        self._running = False
        logger.info("Event bus stopped")
        
    async def _process_event(self, event: Event) -> None:
        """Process a single event."""
        try:
            if event.event_type in self._handlers:
                for handler in self._handlers[event.event_type]:
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(event)
                        else:
                            handler(event)
                    except Exception as e:
                        logger.error(f"Handler error for {event.event_type.value}: {e}", exc_info=True)
                        
        except Exception as e:
            logger.error(f"Error processing event: {e}", exc_info=True)

# Global event bus instance
event_bus = EventBus()

def get_event_bus() -> EventBus:
    """Get the global event bus instance."""
    return event_bus
