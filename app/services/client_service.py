
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.middlewares.track_activity import track_activity
from app.database import db
clientes_bp = Blueprint('clientes', __name__, url_prefix='/api')

client_preferences = [
  {
    "id": 1,
    "cliente_id": 10,
    "idle_timeout_minutes": 30,
    "password_expiration_days": 90,
    "max_login_attempts": 5,
    "refresh_token_expiration_days": 7,
    "enforce_2fa": False,

    "timezone": "America/Santo_Domingo",
    "language": "es",
    "date_format": "DD/MM/YYYY",
    "company_logo_url": "https://example.com/logo_cliente10.png",

    "modules_enabled": {
      "payroll": True,
      "recruitment": True,
      "attendance": False
    },

    "created_at": "2025-01-10T12:30:00",
    "updated_at": "2025-01-15T08:00:00"
  },
  {
    "id": 2,
    "cliente_id": 20,
    "idle_timeout_minutes": 45,
    "password_expiration_days": 60,
    "max_login_attempts": 3,
    "refresh_token_expiration_days": 10,
    "enforce_2fa": True,

    "timezone": "America/Mexico_City",
    "language": "en",
    "date_format": "MM-DD-YYYY",
    "company_logo_url": "https://example.com/logo_cliente20.png",

    "modules_enabled": {
      "payroll": True,
      "recruitment": True,
      "attendance": True,
      "reporting": True
    },

    "created_at": "2025-02-02T14:20:00",
    "updated_at": "2025-02-08T09:50:00"
  }
]



@jwt_required()
@track_activity
def get_client_preferences():
    user_id = get_jwt_identity()  # devuelve lo que enviaste como identity

    # user = user_model.get_user_by_id(user_id=int(user_id))
    is_admin = db.fetch_one("select idrol from usuariosroles where idusuario=%s and idrol=1", (int(user_id),))
    if not is_admin:
        return jsonify({"msg": "Acceso no autorizado"}), 403
    
    
    return client_preferences[0]