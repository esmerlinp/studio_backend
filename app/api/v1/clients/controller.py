from flask import jsonify
from flask_jwt_extended import jwt_required
from app import track_activity

from app.services.client_service import get_client_preferences

#Consumir rutas protegidas con el JWT
#El cliente debe enviar el token en el header: Authorization: Bearer <token>

@jwt_required()
@track_activity
def get_client_preferences():
    preferences = get_client_preferences()
    return jsonify({"result": preferences}), 200


