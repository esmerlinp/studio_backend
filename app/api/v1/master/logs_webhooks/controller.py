from flask import request
from app.services.master_scheme import log_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_logs():
    provider = request.args.get('provider')
    is_processed = request.args.get('is_processed')
    if is_processed is not None:
        is_processed = is_processed.lower() == 'true'
    logs = log_service.get_logs(provider=provider, is_processed=is_processed)
    return success(data=[l.to_dict() for l in logs])

@limiter.limit("60 per minute")
def get_log(log_id):
    log = log_service.get_log_by_id(log_id)
    if not log:
        return error(i18n._("error.log_not_found"), 404)
    return success(data=log.to_dict())

@audit_log(action="create", resource_type="log_webhook")
def create_log():
    data = request.get_json()
    try:
        log = log_service.create_log(
            provider=data.get('provider', 'NEOPAGOS'),
            content=data.get('content'),
            is_processed=data.get('is_processed', False)
        )
        return success(data=log.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="log_webhook", resource_id_arg="log_id")
def update_log(log_id):
    data = request.get_json()
    try:
        log = log_service.update_log_status(log_id, data.get('is_processed', False))
        if not log:
            return error(i18n._("error.log_not_found"), 404)
        return success(data=log.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="log_webhook", resource_id_arg="log_id")
def delete_log(log_id):
    if log_service.delete_log(log_id):
        return success(message=i18n._("success.log_deleted"))
    return error(i18n._("error.log_not_found"), 404)
