from flask import request
from app.api.v1.master.allergies import service as allergy_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_allergies():
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    allergies = allergy_service.get_allergies(active_only=active_only)
    return success(data=[a.to_dict() for a in allergies])

@limiter.limit("60 per minute")
def get_allergy(allergy_id):
    allergy = allergy_service.get_allergy_by_id(allergy_id)
    if not allergy:
        return error(i18n._("error.allergy_not_found"), 404)
    return success(data=allergy.to_dict())

@audit_log(action="create", resource_type="allergy")
def create_allergy():
    data = request.get_json()
    try:
        allergy = allergy_service.create_allergy(
            id=data.get('id'),
            name=data.get('name'),
            is_active=data.get('is_active', True)
        )
        return success(data=allergy.to_dict(), status_code=201)
    except ValueError as e:
        return error(str(e), 400)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="allergy", resource_id_arg="allergy_id")
def update_allergy(allergy_id):
    data = request.get_json()
    try:
        allergy = allergy_service.update_allergy(
            allergy_id,
            name=data.get('name'),
            is_active=data.get('is_active')
        )
        if not allergy:
            return error(i18n._("error.allergy_not_found"), 404)
        return success(data=allergy.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="allergy", resource_id_arg="allergy_id")
def delete_allergy(allergy_id):
    if allergy_service.delete_allergy(allergy_id):
        return success(message=i18n._("success.allergy_deleted"))
    return error(i18n._("error.allergy_not_found"), 404)
