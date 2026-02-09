import logging
from typing import Callable, Dict, List, Any

# Configure logger for event bus
logger = logging.getLogger(__name__)

class EventBus:
    """
    A simple In-Process Event Bus to decouple modules.
    Allows services to emit events and others to subscribe to them.
    """
    _instance = None
    _subscribers: Dict[str, List[Callable]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
            cls._subscribers = {}
        return cls._instance

    def subscribe(self, event_type: str, handler: Callable):
        """
        Subscribe a handler function to an event type.
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        if handler not in self._subscribers[event_type]:
            self._subscribers[event_type].append(handler)
            logger.debug(f"Subscribed {handler.__name__} to {event_type}")

    def emit(self, event_type: str, payload: Any = None):
        """
        Emit an event to all subscribers.
        """
        logger.info(f"Emitting event: {event_type} with payload: {payload}")
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                try:
                    handler(payload)
                except Exception as e:
                    logger.error(f"Error in event handler {handler.__name__} for {event_type}: {str(e)}")

# Global instance
event_bus = EventBus()

def emit_event(event_type: str, payload: Any = None):
    """Utility function to emit event via global bus"""
    event_bus.emit(event_type, payload)

def subscribe_to(event_type: str):
    """Decorator to subscribe a function to an event"""
    def decorator(func):
        event_bus.subscribe(event_type, func)
        return func
    return decorator

# Standardized Event Names
class Events:
    # Health/Nursing
    STUDENT_HEALTH_VISIT = "STUDENT.HEALTH.VISIT"
    STUDENT_HEALTH_CRITICAL = "STUDENT.HEALTH.CRITICAL"
    
    # Cafeteria
    STUDENT_CAFETERIA_PURCHASE = "STUDENT.CAFETERIA.PURCHASE"
    STUDENT_CAFETERIA_ALERT = "STUDENT.CAFETERIA.ALERT"
    
    # Academic
    STUDENT_ATTENDANCE_ABSENT = "STUDENT.ATTENDANCE.ABSENT"
    STUDENT_ATTENDANCE_TARDY = "STUDENT.ATTENDANCE.TARDY"
    STUDENT_ASSIGNMENT_CREATED = "STUDENT.ASSIGNMENT.CREATED"
    
    # Financial
    STUDENT_WALLET_UPDATE = "STUDENT.WALLET.UPDATE"
    STUDENT_DEBT_ALERT = "STUDENT.DEBT.ALERT"
