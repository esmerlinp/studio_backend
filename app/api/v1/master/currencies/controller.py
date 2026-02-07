from flask import request
from app.services.master_scheme import currency_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_currencies():
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    currencies = currency_service.get_currencies(active_only=active_only)
    return success(data=[c.to_dict() for c in currencies])

@limiter.limit("60 per minute")
def get_currency(currency_id):
    currency = currency_service.get_currency_by_id(currency_id)
    if not currency:
        return error(i18n._("error.currency_not_found"), 404)
    return success(data=currency.to_dict())

@audit_log(action="create", resource_type="currency")
def create_currency():
    data = request.get_json()
    try:
        currency = currency_service.create_currency(
            name=data.get('name'),
            iso_code=data.get('iso_code'),
            is_active=data.get('is_active', True)
        )
        return success(data=currency.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="currency", resource_id_arg="currency_id")
def update_currency(currency_id):
    data = request.get_json()
    try:
        currency = currency_service.update_currency(currency_id, **data)
        if not currency:
            return error(i18n._("error.currency_not_found"), 404)
        return success(data=currency.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="currency", resource_id_arg="currency_id")
def delete_currency(currency_id):
    if currency_service.delete_currency(currency_id):
        return success(message=i18n._("success.currency_deleted"))
    return error(i18n._("error.currency_not_found"), 404)
