from flask import jsonify, request
import os
from flask_jwt_extended import jwt_required
from app import track_activity, require_role
from app.utils.responses import error, success
from app.utils.types import Roles as r

LOG_FILE_PATH = 'errors.log'
ADMIN_ROLES = [r.SUPER_ADMIN, r.ROOT]


@jwt_required()
@track_activity
@require_role(ADMIN_ROLES)
def get_logs():
    lines = request.args.get('lines', default=50, type=int)
    
    if not os.path.exists(LOG_FILE_PATH):
        return jsonify({"msg": "El archivo de log no existe aún."}), 404

    try:
        # Leemos el archivo de atrás hacia adelante (las más recientes primero)
        with open(LOG_FILE_PATH, 'r') as f:
            content = f.readlines()
            # Tomamos las últimas 'n' líneas
            last_lines = content[-lines:]
            
        return success(data= {
            "filename": LOG_FILE_PATH,
            "total_lines_returned": len(last_lines),
            "logs": last_lines
        })
    except Exception as e:
        return error(message=str(e), status_code=500)