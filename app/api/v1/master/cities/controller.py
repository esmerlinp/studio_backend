from flask import request
from app.services.master_scheme import city_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_cities():
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    country_id = request.args.get('country_id', type=int)
    cities = city_service.get_cities(active_only=active_only, country_id=country_id)
    return success(data=[c.to_dict() for c in cities])

@limiter.limit("60 per minute")
def get_city(city_id):
    city = city_service.get_city_by_id(city_id)
    if not city:
        return error(i18n._("error.city_not_found"), 404)
    return success(data=city.to_dict())

@audit_log(action="create", resource_type="city")
def create_city():
    data = request.get_json()
    try:
        city = city_service.create_city(
            name=data.get('name'),
            country_id=data.get('country_id'),
            is_active=data.get('is_active', True)
        )
        return success(data=city.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="city", resource_id_arg="city_id")
def update_city(city_id):
    data = request.get_json()
    try:
        city = city_service.update_city(
            city_id,
            name=data.get('name'),
            country_id=data.get('country_id'),
            is_active=data.get('is_active')
        )
        if not city:
            return error(i18n._("error.city_not_found"), 404)
        return success(data=city.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="city", resource_id_arg="city_id")
def delete_city(city_id):
    if city_service.delete_city(city_id):
        return success(message=i18n._("success.city_deleted"))
    return error(i18n._("error.city_not_found"), 404)
