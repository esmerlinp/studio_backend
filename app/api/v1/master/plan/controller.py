from flask import request
from app.services.master_scheme import price_list_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity, require_role
from app.services.master_scheme import plan_service
from app.utils.responses import success, error
from app.utils import i18n,types
from app import limiter


@limiter.limit("20 per minute")
def get_plans():
    data = plan_service.get_plans()
    return success(data=[notif.to_dict() for notif in data])

@jwt_required()
@track_activity
@require_role([types.Roles.ROOT, types.Roles.SUPER_ADMIN])
def get_prices_list(plan_id: int = None):
    data = price_list_service.get_price_lists(plan_id)
    return success(data=[notif.to_dict() for notif in data])


@jwt_required()
@track_activity
@require_role([types.Roles.ROOT, types.Roles.SUPER_ADMIN])
def create_plan():
    code = request.json.get("code", None)
    name = request.json.get("name", None)
    description = request.json.get("description", None)
    max_users = request.json.get("max_users", None)
    max_storage_gb = request.json.get("max_storage_gb", None)
    suppor_level = request.json.get("suppor_level", None)
    environment_type = request.json.get("environment_type", None)
    
    data = plan_service.create_plan(code=code, 
                            name=name, 
                            description=description, 
                            max_users=max_users, 
                            max_storage_gb=max_storage_gb, 
                            support_level=suppor_level, 
                            environment_type=environment_type)
    

    return success(data=data.to_dict())


@jwt_required()
@track_activity
@require_role([types.Roles.ROOT, types.Roles.SUPER_ADMIN])
def add_price_list():
    plan_id = request.json.get("plan_id", None)
    billing_cycle = request.json.get("billing_cycle", None)
    price = request.json.get("price", None)
    currency = request.json.get("currency", None)
    price_per_user = request.json.get("price_per_user", None)
    min_users = request.json.get("min_users", None)
    valid_from = request.json.get("valid_from", None)
    valid_to = request.json.get("valid_to", None)
    features_config = request.json.get("features_config", None)
    
    data = price_list_service.create_price_list(plan_id=plan_id,
                                         billing_cycle=billing_cycle,
                                         price=price,
                                         currency=currency,
                                         price_per_user=price_per_user,
                                         min_users=min_users, valid_from=valid_from, valid_to=valid_to, features_config=features_config)
    

    return success(data=data.to_dict())

@jwt_required()
@track_activity
@require_role([types.Roles.ROOT, types.Roles.SUPER_ADMIN])
def update_price(price_id):
    try:
        data = request.get_json()
        updated_price = price_list_service.update_price_list_service(price_id, data)
        return success(data=updated_price.to_dict(), message=i18n._("msg.price.updated"))
    except ValueError as e:
        return error(str(e), 400)
    except Exception as e:
        return error(str(e), 500)


@jwt_required()
@track_activity
@require_role([types.Roles.ROOT, types.Roles.SUPER_ADMIN])
def update_plan_details(plan_id):
    try:
        data = request.get_json()
        updated_plan = plan_service.update_plan(plan_id, **data)
        if not updated_plan:
             return error(i18n._("error.plan.not_found"), 404)
        return success(data=updated_plan.to_dict(), message=i18n._("msg.plan.updated"))
    except ValueError as e:
        return error(str(e), 400)
    except Exception as e:
        return error(str(e), 500)

@jwt_required()
@track_activity
@require_role([types.Roles.ROOT, types.Roles.SUPER_ADMIN])
def toggle_plan_status(plan_id):
    try:
        data = request.get_json()
        is_active = data.get('is_active')
        if is_active is None:
            return error("is_active is required", 400)
            
        updated_plan = plan_service.update_plan(plan_id, is_active=is_active)
        if not updated_plan:
             return error(i18n._("error.plan.not_found"), 404)
             
        action = "activated" if is_active else "deactivated"
        return success(data=updated_plan.to_dict(), message=f"Plan {action} successfully")
    except Exception as e:
        return error(str(e), 500)
