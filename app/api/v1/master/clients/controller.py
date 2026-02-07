from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity, require_role
from app.services.master_scheme.documents_service import export_client_data
from app.services.master_scheme.client_service import (get_client_preferences, get_client_logs, get_logs_by_entity,
                                                       onboard_client_service, storage_info, 
                                                       create_client, get_clients,
                                                       get_client_by_id, get_client_payment_orders,
                                                       request_scheme_deletion, cancel_scheme_deletion, process_scheduled_deletions,
                                                       update_client_details, toggle_client_active_status, set_schema)

from app.services.master_scheme.user_client_service import get_client_by_user, get_users_by_client 
from app.services.master_scheme.client_plan_service import get_active_client_plan, assign_plan_to_client, change_client_plan, get_client_plan_history
from app.services.master_scheme.user_service import get_user_by_id
from app.utils.responses import success
from flask import request, g, current_app
from app.utils.responses import success, error
from app import db, limiter
from sqlalchemy import text
from datetime import date
from app.utils.types import Roles as r
from app.utils import i18n

#Consumir rutas protegidas con el JWT
#El cliente debe enviar el token en el header: Authorization: Bearer <token>
ADMIN_ROLES = [r.OWNER, r.ADMIN, r.SUPER_ADMIN, r.SYS_ADMIN, r.ROOT]

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_my_institution():
    user_id = get_jwt_identity()  
    data = get_client_by_user(user_id=user_id)
    if not data:
        return error(message=i18n._("error.client.not_found"))
    return success(data=data.to_dict())


@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_my_payments():
    user_id = get_jwt_identity()  
    data = get_client_by_user(user_id=user_id)
    if not data:
        return error(message=i18n._("error.client.not_found"), status_code=404)
    payments = get_client_payment_orders(data.clientId)
    
    return success(data=[d.to_dict() for d in payments])

# @jwt_required()
# @track_activity
# @require_role(ADMIN_ROLES)
# def get_my_invoices():
#     user_id = get_jwt_identity()  
#     data = get_client_by_user(user_id=user_id)
#     payments = get_client_payment_orders(data.clientId)
#     
#     return success(data=[d.to_dict() for d in payments])

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_my_personal_logs():    
    log = get_client_logs()
    return success(data=log)

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_my_personal_logs_by_entity(entityName):
    log = get_logs_by_entity(entityName)
    return success(data=[d.to_dict() for d in log])


@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_my_storage_usage():
    identity = get_jwt_identity()  
    client = get_client_by_user(user_id=identity)
    if client:
        storage = storage_info(client_id=client.clientId)
        return success(data=storage.to_dict())
    return success(data={})


@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_my_subscription():
    
    user_id = get_jwt_identity()  
    data = get_client_by_user(user_id=user_id)
    if not data:
        return error(message=i18n._("error.client.not_found"), status_code=404)
    plan = get_active_client_plan(client_id=data.clientId)
    
    if not plan:
        today = date.today()
        plan = assign_plan_to_client(client_id=data.clientId, plan_id=2, price_list_id=2, start_date=today, commit=True)
        
    return success(data=plan.to_dict())



@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_client_preferences():
    preferences = get_client_preferences()
    if not preferences:
        return success(data={}, message=i18n._("error.client.preferences_not_found"), status_code=200)
    return success(data=preferences)


@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_logs():
    logs = get_client_logs()
    return success(data=[log.to_dict() for log in logs])


@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_client_payments(clientId):
    orders = get_client_payment_orders(client_id=clientId)
    return success(data=[o.to_dict() for o in orders])



@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_client_plans(clientId):

    logs = get_client_plan_history(client_id=clientId)
    return success(data=[log.to_dict() for log in logs])

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_plan(clientId):
    plan = get_active_client_plan(client_id=clientId)
    
    
    if not plan:
        from datetime import date
        today = date.today()
        plan = assign_plan_to_client(client_id=clientId, plan_id=2, price_list_id=2, start_date=today, commit=True)
        
    return success(data=plan.to_dict())

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_my_plan():
    user_id = get_jwt_identity()
    client = get_client_by_user(user_id=user_id)
    if not client:
        return error(message=i18n._("error.client.not_found"), status_code=404)
    plan = get_active_client_plan(client_id=client.clientId)
    
    if not plan:
        from datetime import date
        today = date.today()
        plan = assign_plan_to_client(client_id=client.clientId, plan_id=2, price_list_id=2, start_date=today, commit=True)
        
    return success(data=plan.to_dict())

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES)
def change_plan():
    data = request.get_json()
    plan = change_client_plan(client_id=data.get("client_id"), new_plan_id=data.get("new_plan_id"), new_price_list_id=data.get("new_price_list_id"))
        
    return success(data=plan.to_dict())

@jwt_required()
@track_activity
@require_role([r.ROOT])
def get_client(clientId):
    data = get_client_by_id(clientId=clientId)
    if not data:
        error(message="not found")
    return success(data=data.to_dict())




@jwt_required()
@track_activity
@require_role([r.ROOT])
def get_all_clients():
    data = get_clients()
    return success(data=[d.to_dict() for d in data])



@jwt_required()
@track_activity
@require_role([r.ROOT])
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


@limiter.limit("5 per minute") # Muy restrictivo para evitar ataques DoS al crear clientes
def onboard_client():
    try:
        data = request.get_json()
        client_data = data.get("client_data", None)
        admin_user_data = data.get("user_data", None)
        plan_data = data.get("plan_data", None)


        response_data = onboard_client_service(client_data=client_data,
                            admin_user_data=admin_user_data, plan_data=plan_data)
        return success(data=response_data)
    except ValueError as e:
        # ❗ Errores de negocio (validaciones)
        return error(str(e), 400)

    except Exception as e:
        return error(f"{i18n._('error.internal_server')} {str(e)}", 500)
    


import threading

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES)
def handle_export_data():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    client_id = data.get("client_id")

    # Asumimos que g.scheme contiene el esquema actual del cliente
    app = current_app._get_current_object()
    schema = getattr(g, "scheme", None)

    # Si se provee client_id (caso Admin respaldando un cliente específico)
    if client_id:
        client = get_client_by_id(client_id)
        if not client:
            return error(message=i18n._("error.client.not_found"), status_code=404)
        schema = client.schemaName

    if not schema:
        return error(message=i18n._("error.client.schema_not_determined"))

    try:
        
        user = get_user_by_id(user_id)
        #download_url = export_client_data(schema)
        hilo = threading.Thread(target=export_client_data, args=(app, schema, user.email))
        hilo.daemon = True 
        hilo.start()
        
        # # Opcional: Registrar en auditoría
        # log_action(
        #     action="EXPORT",
        #     resource_type="DATABASE",
        #     description=f"El usuario solicitó descarga total de datos del esquema {schema}",
        #     status="DML"
        # )

        return success(
            message=i18n._("msg.export.process_started"),
            data={
                "status": "processing",
                "info": i18n._("msg.export.delivery_notice")
            }
        )

    except Exception as e:
        return error(message=str(e), status_code=500)

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES)
def request_deletion():
    user_id = get_jwt_identity()
    client = get_client_by_user(user_id=user_id)
    if not client:
        return error(message=i18n._("error.client.not_found"), status_code=404)
        
    try:
        updated_client = request_scheme_deletion(client_id=client.clientId)
        return success(data=updated_client.to_dict(), message=i18n._("msg.client.deletion_requested"))
    except ValueError as e:
        return error(str(e), 400)
    except Exception as e:
        return error(str(e), 500)

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES)
def cancel_deletion():
    user_id = get_jwt_identity()
    client = get_client_by_user(user_id=user_id)
    if not client:
        return error(message=i18n._("error.client.not_found"), status_code=404)
        
    try:
        updated_client = cancel_scheme_deletion(client_id=client.clientId)
        return success(data=updated_client.to_dict(), message=i18n._("msg.client.deletion_cancelled"))
    except ValueError as e:
        return error(str(e), 400)
    except Exception as e:
        return error(str(e), 500)

@jwt_required()
@require_role([r.ROOT])
def trigger_cleanup():
    try:
        results = process_scheduled_deletions()
        return success(data=results, message="Cleanup process executed")
    except Exception as e:
        return error(str(e), 500)

@jwt_required()
@track_activity
@require_role([r.ROOT, r.SYS_ADMIN])
def update_client(clientId):
    try:
        data = request.get_json()
        client = update_client_details(client_id=clientId, data=data)
        return success(data=client.to_dict(), message=i18n._("msg.client.updated"))
    except ValueError as e:
        return error(str(e), 400)
    except Exception as e:
        return error(str(e), 500)

@jwt_required()
@track_activity
@require_role([r.ROOT, r.SYS_ADMIN])
def toggle_client_status(clientId):
    try:
        data = request.get_json()
        is_active = data.get('is_active')
        if is_active is None:
            return error("is_active is required", 400)
            
        client = toggle_client_active_status(client_id=clientId, is_active=is_active)
        return success(data=client.to_dict(), message=i18n._("msg.client.status_updated"))
    except ValueError as e:
        return error(str(e), 400)
    except Exception as e:
        return error(str(e), 500)

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_client_storage(clientId):
    storage = storage_info(client_id=clientId)
    if storage:
        return success(data=storage.to_dict())
    return success(data={})

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_client_users(clientId):
    client = get_client_by_id(clientId)
    if not client:
        return error(i18n._("error.client.not_found"), 404)
        
    relations = get_users_by_client(client_uuid=client.uuid)
    
    users_data = []
    for rel in relations:
        user = get_user_by_id(rel.user_id)
        if user:
            u_dict = user.to_dict()
            users_data.append(u_dict)
            
    return success(data=users_data)

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES + [r.AUDITOR])
def get_client_logs_admin(clientId):
    try:
        client = get_client_by_id(clientId)
        if not client:
            return error(i18n._("error.client.not_found"), 404)

        current_schema = getattr(g, 'scheme', 'public') 
        target_schema = client.schemaName
        
        set_schema(target_schema)
        
        # Obtener filtros de la URL
        action = request.args.get('action')
        resource_type = request.args.get('resource_type')
        user_id = request.args.get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        logs = get_client_logs(
            action=action, 
            resource_type=resource_type, 
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        ) 
        
        set_schema(current_schema)
        
        # Retornar TODA la respuesta (data + meta)
        return success(data=logs)
        
    except Exception as e:
        try:
             current_schema = getattr(g, 'scheme', 'public')
             set_schema(current_schema)
        except:
            pass
        return error(str(e), 500)