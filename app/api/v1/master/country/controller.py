from flask import request
from app.services.master_scheme import country_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_countries():
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    countries = country_service.get_countries(active_only=active_only)
    return success(data=[c.to_dict() for c in countries])

@limiter.limit("60 per minute")
def get_country(country_id):
    country = country_service.get_country_by_id(country_id)
    if not country:
        return error(i18n._("error.country_not_found"), 404)
    return success(data=country.to_dict())

@audit_log(action="create", resource_type="country")
def create_country():
    data = request.get_json()
    try:
        country = country_service.create_country(
            name=data.get('name'),
            iso_code=data.get('iso_code'),
            is_active=data.get('is_active', True)
        )
        return success(data=country.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="country", resource_id_arg="country_id")
def update_country(country_id):
    data = request.get_json()
    try:
        country = country_service.update_country(country_id, **data)
        if not country:
            return error(i18n._("error.country_not_found"), 404)
        return success(data=country.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="country", resource_id_arg="country_id")
def delete_country(country_id):
    if country_service.delete_country(country_id):
        return success(message=i18n._("success.country_deleted"))
    return error(i18n._("error.country_not_found"), 404)