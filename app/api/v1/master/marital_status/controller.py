from flask import request
from app.services.master_scheme import marital_status_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_marital_statuses():
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    statuses = marital_status_service.get_marital_statuses(active_only=active_only)
    return success(data=[s.to_dict() for s in statuses])

@limiter.limit("60 per minute")
def get_marital_status(status_id):
    status = marital_status_service.get_marital_status_by_id(status_id)
    if not status:
        return error(i18n._("error.marital_status_not_found"), 404)
    return success(data=status.to_dict())

@audit_log(action="create", resource_type="marital_status")
def create_marital_status():
    data = request.get_json()
    try:
        status = marital_status_service.create_marital_status(
            name=data.get('name'),
            is_active=data.get('is_active', True)
        )
        return success(data=status.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="marital_status", resource_id_arg="status_id")
def update_marital_status(status_id):
    data = request.get_json()
    try:
        status = marital_status_service.update_marital_status(
            status_id,
            name=data.get('name'),
            is_active=data.get('is_active')
        )
        if not status:
            return error(i18n._("error.marital_status_not_found"), 404)
        return success(data=status.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="marital_status", resource_id_arg="status_id")
def delete_marital_status(status_id):
    if marital_status_service.delete_marital_status(status_id):
        return success(message=i18n._("success.marital_status_deleted"))
    return error(i18n._("error.marital_status_not_found"), 404)
