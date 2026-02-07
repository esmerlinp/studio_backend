from flask import request
from app.services.master_scheme import bank_service
from app.utils.responses import success, error
from app import limiter, audit_log
from app.utils import i18n

@limiter.limit("60 per minute")
def get_banks():
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    banks = bank_service.get_banks(active_only=active_only)
    return success(data=[b.to_dict() for b in banks])

@limiter.limit("60 per minute")
def get_bank(bank_id):
    bank = bank_service.get_bank_by_id(bank_id)
    if not bank:
        return error(i18n._("error.bank_not_found"), 404)
    return success(data=bank.to_dict())

@audit_log(action="create", resource_type="bank")
def create_bank():
    data = request.get_json()
    try:
        bank = bank_service.create_bank(
            name=data.get('name'),
            is_active=data.get('is_active', True)
        )
        return success(data=bank.to_dict(), status_code=201)
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="update", resource_type="bank", resource_id_arg="bank_id")
def update_bank(bank_id):
    data = request.get_json()
    try:
        bank = bank_service.update_bank(
            bank_id,
            name=data.get('name'),
            is_active=data.get('is_active')
        )
        if not bank:
            return error(i18n._("error.bank_not_found"), 404)
        return success(data=bank.to_dict())
    except Exception as e:
        return error(str(e), 500)

@audit_log(action="delete", resource_type="bank", resource_id_arg="bank_id")
def delete_bank(bank_id):
    if bank_service.delete_bank(bank_id):
        return success(message=i18n._("success.bank_deleted"))
    return error(i18n._("error.bank_not_found"), 404)
