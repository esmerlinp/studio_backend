from flask import request
from app.services import plan_service, price_list_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity
from app.utils.responses import success, error
from app.utils import i18n




def get_plans():
    data = plan_service.get_plans()
    return success(data=[notif.to_dict() for notif in data])

def get_prices_list(plan_id: int = None):
    data = price_list_service.get_price_lists(plan_id)
    return success(data=[notif.to_dict() for notif in data])



@jwt_required()
@track_activity
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
def add_price_list():
    plan_id = request.json.get("plan_id", None)
    billing_cycle = request.json.get("billing_cycle", None)
    price = request.json.get("price", None)
    currency = request.json.get("currency", None)
    price_per_user = request.json.get("price_per_user", None)
    min_users = request.json.get("min_users", None)
    valid_from = request.json.get("valid_from", None)
    valid_to = request.json.get("valid_to", None)
    
    data = price_list_service.create_price_list(plan_id=plan_id,
                                         billing_cycle=billing_cycle,
                                         price=price,
                                         currency=currency,
                                         price_per_user=price_per_user,
                                         min_users=min_users, valid_from=valid_from, valid_to=valid_to)
    

    return success(data=data.to_dict())

    
@jwt_required()
@track_activity
def mark_read():
    user_id = get_jwt_identity()
    notif_id = request.json.get("notif_id", None)
    if not notif_id:
        return error(message=i18n._("api.notifications.missing_notif_id"), status_code=400)
    
    data = notification_service.mark_read(user_id=user_id, notif_id=notif_id)
    return success(data=data.to_dict(), message=i18n._("api.notifications.marked_as_read"), status_code=200)