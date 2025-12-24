from flask import request
from app.services.master_scheme import user_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity
from app.services.master_scheme import auth_service, session_service
from app.utils.responses import success, error
from app.utils import i18n

@jwt_required()
def sessions():
    try:
        user_id = get_jwt_identity()
        sessions = session_service.get_open_sessions(user_id=int(user_id))
        data = [s.to_dict() for s in sessions]
        return success(data=data, message=i18n._("common.open_sessions_retrieved_successfully"), status_code=200)
    except Exception as e:
        return error(message=str(e), status_code=500)


@jwt_required()
@track_activity
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
@track_activity
def logout(sessionId):
    try:
        user_id = get_jwt_identity()
        sessions = session_service.close_session(sessionId=sessionId, user_id=int(user_id))
        return success(data=sessions, message=i18n._("common.session_closed_successfully"), status_code=200)
    except Exception as e:
        return error(message=str(e), status_code=500)


@jwt_required(refresh=True)
@track_activity
def refresh_token():
    try:
        identity = get_jwt_identity()     # recupera el mismo identity guardado en el refresh token
        result = auth_service.refresh_token(user_id=int(identity))
        
        return success(data=result, message=i18n._("common.token_refreshed_successfully"), status_code=200)
    except Exception as e:
        return error(message=str(e), status_code=500)
    


    
