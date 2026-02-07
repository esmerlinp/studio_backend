from flask import request
from app.services.master_scheme import health_insurance_institution_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_health_insurance_institutions():
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    insts = health_insurance_institution_service.get_health_insurance_institutions(active_only=active_only)
    return success(data=[i.to_dict() for i in insts])

@limiter.limit("60 per minute")
def get_health_insurance_institution(inst_id):
    inst = health_insurance_institution_service.get_health_insurance_institution_by_id(inst_id)
    if not inst:
        return error(i18n._("error.health_insurance_institution_not_found"), 404)
    return success(data=inst.to_dict())

@audit_log(action="create", resource_type="health_insurance_institution")
def create_health_insurance_institution():
    data = request.get_json()
    try:
        inst = health_insurance_institution_service.create_health_insurance_institution(
            name=data.get('name'),
            is_active=data.get('is_active', True)
        )
        return success(data=inst.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="health_insurance_institution", resource_id_arg="inst_id")
def update_health_insurance_institution(inst_id):
    data = request.get_json()
    try:
        inst = health_insurance_institution_service.update_health_insurance_institution(
            inst_id,
            name=data.get('name'),
            is_active=data.get('is_active')
        )
        if not inst:
            return error(i18n._("error.health_insurance_institution_not_found"), 404)
        return success(data=inst.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="health_insurance_institution", resource_id_arg="inst_id")
def delete_health_insurance_institution(inst_id):
    if health_insurance_institution_service.delete_health_insurance_institution(inst_id):
        return success(message=i18n._("success.health_insurance_institution_deleted"))
    return error(i18n._("error.health_insurance_institution_not_found"), 404)
