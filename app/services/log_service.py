from flask import request
from flask_jwt_extended import get_jwt_identity
from app.models.client.log_model import AuditLog
from ..extensions import db


def log_action(
    action: str,
    resource_type: str,
    resource_id: int | None = None,
    description: str | None = None,
    old_values: dict | None = None,
    new_values: dict | None = None,
):
    try:
        audit = AuditLog(
            user_id=get_jwt_identity(),
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent"),
            old_values=old_values,
            new_values=new_values
        )
        db.session.add(audit)
        db.session.commit()
    except Exception:
        db.session.rollback()
