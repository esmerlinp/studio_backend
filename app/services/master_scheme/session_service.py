
from app.models.master_scheme.session_model import Session
from typing import Optional
from datetime import  timedelta
from ...extensions import db 
from datetime import datetime, timezone
from app.utils import i18n

# @audit_log(action=ActionType.CREATE,
#            resource_type=ResourceTypes.USER_SESSION,
#            resource_id_arg="userId")
def create_session(userId: int, refreshToken: str, inactivity_minutes:int, ipAddress:str, userAgent:str = None) -> Session:
    now = datetime.now(timezone.utc)
    session = Session(
        userId=userId,
        refreshToken=refreshToken,
        expirationDate=now + timedelta(minutes=inactivity_minutes),
        lastAccessDate=now,
        ipAddress = ipAddress,
        userAgent = userAgent,
        isActive=True
    )
    db.session.add(session)
    db.session.commit()
    return session


# @audit_log(action=ActionType.READ,
#            resource_type=ResourceTypes.USER_SESSION,
#            resource_id_arg="userId", description="Consultar session por id usuario")
def get_session_active_by_user_id(userId: int)->Optional[Session]:
    session = Session.query.filter_by(userId=userId, isActive=True).order_by(Session.sessionId.desc()).first()
    if not session:
        return None
    
    return session

def get_session_active_by_refresh_token(refreshToken:str)->Optional[Session]:
    session = Session.query.filter_by(refreshToken=refreshToken, isActive=True).first()
    if not session:
        return None
    
    return session

# @audit_log(action=ActionType.UPDATE,
#            resource_type=ResourceTypes.USER_SESSION,
#            resource_id_arg="sessionId")
def invalidar_sesiones_por_id_session(sessionId: int):
    session = Session.query.filter_by(sessionId=sessionId).first()
    if session:
        session.isActive = False

        db.session.commit()
    return True

# @audit_log(action=ActionType.UPDATE,
#            resource_type=ResourceTypes.USER_SESSION,
#            resource_id_arg="sessionId")
def actualizar_actividad_sesion(sessionId: int, inactivity_minutes: int):
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
            
    session = Session.query.filter_by(sessionId=sessionId).first()
    if session:

        session.lastAccessDate = now
        session.expirationDate = now + timedelta(minutes=inactivity_minutes)
        

        db.session.commit()
    return True

    # database.execute_non_query("""
    #     UPDATE usuariossesiones 
    #     SET dultimoacceso = %s,
    #         dfechaexpiracion = %s
    #     WHERE idusuariosesion = %s
    # """, (
    #     now,
    #     now + timedelta(minutes=INACTIVITY_MINUTES),
    #     session["idusuariosesion"]
    # ))
    

from typing import List, Optional
# @audit_log(action=ActionType.READ,
#            resource_type=ResourceTypes.USER_SESSION,
#            resource_id_arg="user_id", description="consultar sessiones abiertas por id usuario")
def get_open_sessions(user_id: int) -> List[Optional[Session]]:
    now = datetime.now(timezone.utc)
    #rows = db.fetch_data("SELECT * FROM usuariossesiones where bactivo = TRUE AND idusuario = %s", (int(user_id), ))
    sessions = Session.query.filter(
        Session.userId == int(user_id),
        Session.isActive == True,
        Session.expirationDate > now
    ).all()
    return sessions

# @audit_log(action=ActionType.UPDATE,
#            resource_type=ResourceTypes.USER_SESSION,
#            resource_id_arg="sessionId", description="Cerrar session")
def close_session(sessionId, user_id:int) -> dict:
    #value = db.execute_non_query("UPDATE usuariossesiones SET bactivo = FALSE WHERE idusuariosesion = %s AND idusuario = %s", (sessionId, int(user_id), ))
    session = Session.query.filter_by(sessionId=sessionId, userId=user_id).first()
    if session:
        session.isActive = False
        db.session.commit()
        
    return {"sessionId": sessionId}


# @audit_log(action=ActionType.UPDATE,
#            resource_type=ResourceTypes.USER_SESSION,
#            resource_id_arg="sessionId", description="Cerrar todas las sesiones excepto actual")
def close_all_session_except_current(sessionId, user_id:int) -> dict:
    """Cierra todas las sesiones activas de un usuario excepto la actual"""
    #value = db.execute_non_query("UPDATE usuariossesiones SET bactivo = FALSE WHERE idusuariosesion <> %s AND idusuario = %s", (sessionId, int(user_id), ))
    sessions = Session.query.filter(Session.sessionId != sessionId, Session.userId == user_id).all()
    if sessions:
        for session in sessions:
            session.isActive = False
        db.session.commit()
        
    # if value == 0:
    #     return {"sessionId": 0}
    
    return {"sessionId": sessionId}


# @audit_log(action=ActionType.UPDATE,
#            resource_type=ResourceTypes.USER_SESSION,
#            resource_id_arg="user_id", description="Cerrar todas las sesiones del usuario")
def close_all_session(user_id: int, commit = True) -> dict:
    """Cierra todas las sesiones activas de un usuario de forma masiva"""
    try:
        # Realizamos el update de todas las sesiones activas de ese usuario en un solo paso
        updated_count = Session.query.filter_by(userId=user_id, isActive=True).update(
            {"isActive": False},
            synchronize_session=False
        )
        if commit:
            db.session.commit()
        
        return {
            "status": "success", 
            "message": i18n._("auth.sessions_closed_count") % updated_count,
            "user_id": user_id
        }
    except Exception as e:
        if commit:
            db.session.rollback()
        return {"status": "error", "message": str(e)}