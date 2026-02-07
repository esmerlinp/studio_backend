from typing import List, Optional
from app.extensions import db
from app.models.master_scheme.log_webhook_model import LogWebhook
from flask import request

def log_action(action, resource_type, resource_id=None, description=None, old_values=None, new_values=None, user_id=None, status="DML"):
    """
    Registra una acción en el log de auditoría.
    """
    from app.models.client_scheme.log_model import AuditLog
    
    try:
        log = AuditLog(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            old_values=old_values,
            new_values=new_values,
            user_id=user_id,
            accion_type=status,
            ip_address=request.remote_addr if request else None,
            user_agent=request.user_agent.string if request and request.user_agent else None
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error saving audit log: {e}")

def get_logs(provider: Optional[str] = None, is_processed: Optional[bool] = None) -> List[LogWebhook]:
    query = LogWebhook.query
    if provider:
        query = query.filter(LogWebhook.provider == provider)
    if is_processed is not None:
        query = query.filter(LogWebhook.is_processed == is_processed)
    return query.order_by(LogWebhook.created_at.desc()).all()

def get_log_by_id(log_id: int) -> Optional[LogWebhook]:
    return LogWebhook.query.get(log_id)

def create_log(*, provider: str = 'NEOPAGOS', content: dict, is_processed: bool = False) -> LogWebhook:
    log = LogWebhook(provider=provider, content=content, is_processed=is_processed)
    db.session.add(log)
    try:
        db.session.commit()
        return log
    except Exception as e:
        db.session.rollback()
        raise e

def update_log_status(log_id: int, is_processed: bool) -> Optional[LogWebhook]:
    log = get_log_by_id(log_id)
    if not log:
        return None
    log.is_processed = is_processed
    try:
        db.session.commit()
        return log
    except Exception as e:
        db.session.rollback()
        raise e

def delete_log(log_id: int) -> bool:
    log = get_log_by_id(log_id)
    if not log:
        return False
    db.session.delete(log)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e