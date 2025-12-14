from flask_jwt_extended import jwt_required
from app import track_activity
from app.services.client_service import get_client_preferences
from app.utils.responses import success

#Consumir rutas protegidas con el JWT
#El cliente debe enviar el token en el header: Authorization: Bearer <token>

@jwt_required()
@track_activity
def get_client_preferences():
    preferences = get_client_preferences()
    if not preferences:
        return success(data={}, message="Client preferences not found", status_code=200)
    return success(data=preferences, message="Client preferences retrieved successfully", status_code=200)


