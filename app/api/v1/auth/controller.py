from flask import jsonify
from app.services import user_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity
from app.services import auth_service


@jwt_required()
def sessions():
    user_id = get_jwt_identity()
    sessions = user_service.get_open_sessions(user_id=int(user_id))
    return jsonify({"result": sessions})


@jwt_required()
@track_activity
def close_session(sessionId):
    user_id = get_jwt_identity()
    sessions = user_service.close_session(sessionId=sessionId, user_id=int(user_id))
    return jsonify({"result": sessions})



def login():
    return auth_service.login()


def logout():
    # TODO: gestionar invalidación del token en tabla de sesiones
    return jsonify({"result": "ok"}), 200


@jwt_required(refresh=True)
@track_activity
def refresh_token():
    identity = get_jwt_identity()     # recupera el mismo identity guardado en el refresh token
    result = auth_service.refresh_token(user_id=int(identity))
    
    return jsonify({'result': result}), 200
