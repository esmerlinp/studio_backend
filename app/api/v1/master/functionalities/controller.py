from flask import request
from app.services.master_scheme import functionality_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_functionalities():
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    funcs = functionality_service.get_functionalities(active_only=active_only)
    return success(data=[f.to_dict() for f in funcs])

@limiter.limit("60 per minute")
def get_functionality(func_id):
    func = functionality_service.get_functionality_by_id(func_id)
    if not func:
        return error(i18n._("error.functionality_not_found"), 404)
    return success(data=func.to_dict())

@audit_log(action="create", resource_type="functionality")
def create_functionality():
    data = request.get_json()
    try:
        func = functionality_service.create_functionality(
            name=data.get('name'),
            description=data.get('description'),
            code=data.get('code'),
            is_active=data.get('is_active', True)
        )
        return success(data=func.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="functionality", resource_id_arg="func_id")
def update_functionality(func_id):
    data = request.get_json()
    try:
        func = functionality_service.update_functionality(
            func_id,
            name=data.get('name'),
            description=data.get('description'),
            code=data.get('code'),
            is_active=data.get('is_active')
        )
        if not func:
            return error(i18n._("error.functionality_not_found"), 404)
        return success(data=func.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="functionality", resource_id_arg="func_id")
def delete_functionality(func_id):
    if functionality_service.delete_functionality(func_id):
        return success(message=i18n._("success.functionality_deleted"))
    return error(i18n._("error.functionality_not_found"), 404)
