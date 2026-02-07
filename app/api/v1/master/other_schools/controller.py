from flask import request
from app.services.master_scheme import other_school_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_other_schools():
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    schools = other_school_service.get_other_schools(active_only=active_only)
    return success(data=[s.to_dict() for s in schools])

@limiter.limit("60 per minute")
def get_other_school(school_id):
    school = other_school_service.get_other_school_by_id(school_id)
    if not school:
        return error(i18n._("error.school_not_found"), 404)
    return success(data=school.to_dict())

@audit_log(action="create", resource_type="other_school")
def create_other_school():
    data = request.get_json()
    try:
        school = other_school_service.create_other_school(
            id=data.get('id'),
            name=data.get('name'),
            is_active=data.get('is_active', True)
        )
        return success(data=school.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="other_school", resource_id_arg="school_id")
def update_other_school(school_id):
    data = request.get_json()
    try:
        school = other_school_service.update_other_school(school_id, **data)
        if not school:
            return error(i18n._("error.school_not_found"), 404)
        return success(data=school.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="other_school", resource_id_arg="school_id")
def delete_other_school(school_id):
    if other_school_service.delete_other_school(school_id):
        return success(message=i18n._("success.school_deleted"))
    return error(i18n._("error.school_not_found"), 404)
