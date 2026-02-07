from flask import request
from app.services.master_scheme import month_name_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_months():
    months = month_name_service.get_month_names()
    return success(data=[m.to_dict() for m in months])

@limiter.limit("60 per minute")
def get_month(month_id):
    month = month_name_service.get_month_by_id(month_id)
    if not month:
        return error(i18n._("error.month_not_found"), 404)
    return success(data=month.to_dict())

@audit_log(action="create", resource_type="month_name")
def create_month():
    data = request.get_json()
    try:
        month = month_name_service.create_month(
            month_num=data.get('month_num'),
            name=data.get('name'),
            short_name=data.get('short_name')
        )
        return success(data=month.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="month_name", resource_id_arg="month_id")
def update_month(month_id):
    data = request.get_json()
    try:
        month = month_name_service.update_month(month_id, **data)
        if not month:
            return error(i18n._("error.month_not_found"), 404)
        return success(data=month.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="month_name", resource_id_arg="month_id")
def delete_month(month_id):
    if month_name_service.delete_month(month_id):
        return success(message=i18n._("success.month_deleted"))
    return error(i18n._("error.month_not_found"), 404)
