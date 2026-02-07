from flask import request
from app.services.master_scheme import module_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_modules():
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    modules = module_service.get_modules(active_only=active_only)
    return success(data=[m.to_dict() for m in modules])

@limiter.limit("60 per minute")
def get_module(module_id):
    module = module_service.get_module_by_id(module_id)
    if not module:
        return error(i18n._("error.module_not_found"), 404)
    return success(data=module.to_dict())

@audit_log(action="create", resource_type="module")
def create_module():
    data = request.get_json()
    try:
        module = module_service.create_module(
            name=data.get('name'),
            description=data.get('description'),
            icon=data.get('icon'),
            order=data.get('order'),
            is_active=data.get('is_active', True)
        )
        return success(data=module.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="module", resource_id_arg="module_id")
def update_module(module_id):
    data = request.get_json()
    try:
        module = module_service.update_module(module_id, **data)
        if not module:
            return error(i18n._("error.module_not_found"), 404)
        return success(data=module.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="module", resource_id_arg="module_id")
def delete_module(module_id):
    if module_service.delete_module(module_id):
        return success(message=i18n._("success.module_deleted"))
    return error(i18n._("error.module_not_found"), 404)
