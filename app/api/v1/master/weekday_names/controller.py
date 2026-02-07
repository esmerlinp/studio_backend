from flask import request
from app.services.master_scheme import weekday_name_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_weekdays():
    weekdays = weekday_name_service.get_weekday_names()
    return success(data=[w.to_dict() for w in weekdays])

@limiter.limit("60 per minute")
def get_weekday(weekday_id):
    weekday = weekday_name_service.get_weekday_by_id(weekday_id)
    if not weekday:
        return error(i18n._("error.weekday_not_found"), 404)
    return success(data=weekday.to_dict())

@audit_log(action="create", resource_type="weekday_name")
def create_weekday():
    data = request.get_json()
    try:
        weekday = weekday_name_service.create_weekday(
            weekday_num=data.get('weekday_num'),
            name=data.get('name'),
            short_name=data.get('short_name')
        )
        return success(data=weekday.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="weekday_name", resource_id_arg="weekday_id")
def update_weekday(weekday_id):
    data = request.get_json()
    try:
        weekday = weekday_name_service.update_weekday(weekday_id, **data)
        if not weekday:
            return error(i18n._("error.weekday_not_found"), 404)
        return success(data=weekday.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="weekday_name", resource_id_arg="weekday_id")
def delete_weekday(weekday_id):
    if weekday_name_service.delete_weekday(weekday_id):
        return success(message=i18n._("success.weekday_deleted"))
    return error(i18n._("error.weekday_not_found"), 404)
