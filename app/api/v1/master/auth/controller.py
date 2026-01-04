
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity, track_and_log, audit_log
from app.services.master_scheme import auth_service, session_service
from app.utils.responses import success, error
from app.utils import i18n
from app.utils.types import ActionType, ResourceTypes

@jwt_required()
@track_and_log(
    action=ActionType.READ, 
    resource_type=ResourceTypes.USER_SESSION, 
    description="Consultar sessiones"
)
def sessions():
    try:
        user_id = get_jwt_identity()
        sessions = session_service.get_open_sessions(user_id=int(user_id))
        data = [s.to_dict() for s in sessions]
        return success(data=data, message=i18n._("common.open_sessions_retrieved_successfully"), status_code=200)
    except Exception as e:
        return error(message=str(e), status_code=500)


@jwt_required()
@track_and_log(
    action=ActionType.LOGOUT, 
    resource_type=ResourceTypes.USER_SESSION, 
    resource_id_arg="sessionId",
    description="cerrar session"
)
def close_session(sessionId):
    try:
        user_id = get_jwt_identity()
        sessions = session_service.close_session(sessionId=sessionId, user_id=int(user_id))
        return success(data=sessions, message=i18n._("common.session_closed_successfully"), status_code=200)
    except Exception as e:
        return error(message=str(e), status_code=500)


def login():
    return auth_service.login()


@jwt_required()
@track_and_log(
    action=ActionType.LOGOUT, 
    resource_type=ResourceTypes.USER_SESSION, 
    description="Salir del sistema"
)
def logout(sessionId):
    try:
        user_id = get_jwt_identity()
        sessions = session_service.close_session(sessionId=sessionId, user_id=int(user_id))
        return success(data=sessions, message=i18n._("common.session_closed_successfully"), status_code=200)
    except Exception as e:
        return error(message=str(e), status_code=500)


@jwt_required(refresh=True)
@track_and_log(
    action=ActionType.UPDATE, 
    resource_type=ResourceTypes.USER_SESSION, 
    description="Generar nuevo token (refresh_token)"
)
def refresh_token():
    try:
        identity = get_jwt_identity()     # recupera el mismo identity guardado en el refresh token
        result = auth_service.refresh_token(user_id=int(identity))
        
        return success(data=result, message=i18n._("common.token_refreshed_successfully"), status_code=200)
    except Exception as e:
        return error(message=str(e), status_code=500)
    


    
