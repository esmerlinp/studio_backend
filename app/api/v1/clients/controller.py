from flask_jwt_extended import jwt_required
from app import track_activity
from app.services.client_service import get_client_preferences, get_client_logs
from app.utils.responses import success
from app.services.client_service import create_client
from flask import request
from app.utils.responses import success, error


#Consumir rutas protegidas con el JWT
#El cliente debe enviar el token en el header: Authorization: Bearer <token>


@jwt_required()
@track_activity
def get_client_preferences():
    preferences = get_client_preferences()
    if not preferences:
        return success(data={}, message="Client preferences not found", status_code=200)
    return success(data=preferences)


@jwt_required()
@track_activity
def get_logs():

    logs = get_client_logs()
    return success(data=[log.to_dict() for log in logs])


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
