from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity, require_role
from app.services.master_scheme.client_service import get_client_preferences, get_client_logs, onboard_client_service, storage_info, create_client, get_clients, get_client_by_id, get_client_by_uuid
from app.services.master_scheme.user_client_service import get_client_by_user   
from app.services.master_scheme.client_plan_service import get_active_client_plan, assign_plan_to_client, change_client_plan
from app.utils.responses import success
from flask import request
from app.utils.responses import success, error


#Consumir rutas protegidas con el JWT
#El cliente debe enviar el token en el header: Authorization: Bearer <token>


@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN"])
def get_client_preferences():
    preferences = get_client_preferences()
    if not preferences:
        return success(data={}, message="Client preferences not found", status_code=200)
    return success(data=preferences)


@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN", "SUPPORT"])
def get_logs():

    logs = get_client_logs()
    return success(data=[log.to_dict() for log in logs])

@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN", "SUPPORT"])
def get_plan(clientId):
    plan = get_active_client_plan(client_id=clientId)
    
    
    if not plan:
        from datetime import date
        today = date.today()
        plan = assign_plan_to_client(client_id=clientId, plan_id=2, price_list_id=2, start_date=today, commit=True)
        
    return success(data=plan.to_dict())

@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN", "SUPPORT"])
def change_plan():
    data = request.get_json()
    plan = change_client_plan(**data)
        
    return success(data=plan.to_dict())

@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN", "SUPPORT"])
def get_client(clientId):
    data = get_client_by_id(clientId=clientId)
    if not data:
        error(message="not found")
    return success(data=data.to_dict())

@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN", "SUPPORT"])
def get_clients():
    data = get_clients()
    return success(data=[d.to_dict() for d in data])

@jwt_required()
@track_activity
def get_storage_info():
    identity = get_jwt_identity()  
    client = get_client_by_user(user_id=identity)
    storage = storage_info(client_id=client.clientId)
    return success(data=storage.to_dict())


@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN"])
def new_cliente():
    data = request.get_json()

    client = create_client(
        name=data.get("name"),
        contact_name=data.get("contact_name"),
        phone_type_id=data.get("phone_type_id"),
        contact_phone=data.get("contact_phone"),
        document_type_id=data.get("document_type_id"),
        document_number=data.get("document_number"),
        business_name=data.get("business_name"),
        billing_country_id=data.get("billing_country_id"),
        billing_city_id=data.get("billing_city_id"),
        billing_sector_id=data.get("billing_sector_id"),
        billing_address=data.get("billing_address"),
        billing_email=data.get("billing_email"),
        service_start_date=data.get("service_start_date"),
        comment=data.get("comment"),
        schema_name=data.get("schema_name"),
        is_active=data.get("is_active", True)
    )

    return success(data=client.to_dict())


def onboard_client():
    try:
        data = request.get_json()
        client_data = data.get("client_data", None)
        admin_user_data = data.get("user_data", None)


        response_data = onboard_client_service(client_data=client_data,
                            admin_user_data=admin_user_data)
        return success(data=response_data.to_dict())
    except ValueError as e:
        # ❗ Errores de negocio (validaciones)
        return error(str(e), 400)

    except Exception as e:
        # ❗ Error inesperado
        
        return error(f"Error interno del servidor {e}", 500)
    
    