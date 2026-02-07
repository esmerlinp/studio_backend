from flask import request
from app.services.master_scheme import function_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_functions():
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    funcs = function_service.get_functions(active_only=active_only)
    return success(data=[f.to_dict() for f in funcs])

@limiter.limit("60 per minute")
def get_function(func_id):
    func = function_service.get_function_by_id(func_id)
    if not func:
        return error(i18n._("error.function_not_found"), 404)
    return success(data=func.to_dict())

@audit_log(action="create", resource_type="function")
def create_function():
    data = request.get_json()
    try:
        func = function_service.create_function(
            name=data.get('name'),
            description=data.get('description'),
            example=data.get('example'),
            is_active=data.get('is_active', True)
        )
        return success(data=func.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="function", resource_id_arg="func_id")
def update_function(func_id):
    data = request.get_json()
    try:
        func = function_service.update_function(
            func_id,
            name=data.get('name'),
            description=data.get('description'),
            example=data.get('example'),
            is_active=data.get('is_active')
        )
        if not func:
            return error(i18n._("error.function_not_found"), 404)
        return success(data=func.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="function", resource_id_arg="func_id")
def delete_function(func_id):
    if function_service.delete_function(func_id):
        return success(message=i18n._("success.function_deleted"))
    return error(i18n._("error.function_not_found"), 404)
