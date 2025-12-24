
from app.models.master_scheme.session_model import Session
from typing import Optional
from datetime import  timedelta
from ...extensions import db 
from datetime import datetime, timezone


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

def invalidar_sesiones_por_id_session(sessionId: int):
    session = Session.query.filter_by(sessionId=sessionId).first()
    
    if session:
        session.isActive = False
        db.session.commit()
    return True

def actualizar_actividad_sesion(sessionId: int, inactivity_minutes: int):
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
            
    session = Session.query.filter_by(sessionId=sessionId).first()
    if session:
        from datetime import datetime
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
def get_open_sessions(user_id: int) -> List[Optional[Session]]:
    #rows = db.fetch_data("SELECT * FROM usuariossesiones where bactivo = TRUE AND idusuario = %s", (int(user_id), ))
    sessions = Session.query.filter_by(userId=int(user_id), isActive=True).all()

    # sessions = []
    # for s in rows:
    #     sessions.append(
    #         {
    #             "sessionId": s.get("idusuariosesion", 0),
    #             "lastAccess": s.get("dultimoacceso", None),
    #             "expired": s.get("dfechaexpiracion", None),
    #             "device": f"Random device {s.get("idusuariosesion", 0)}",
    #             "deviceIp": request.remote_addr #TODO: sustituir por campo real cuando se implemente
    #         }
    #     )

    return sessions

def close_session(sessionId, user_id:int) -> dict:
    #value = db.execute_non_query("UPDATE usuariossesiones SET bactivo = FALSE WHERE idusuariosesion = %s AND idusuario = %s", (sessionId, int(user_id), ))
    session = Session.query.filter_by(sessionId=sessionId, userId=user_id).first()
    if session:
        session.isActive = False
        db.session.commit()
        
    return {"sessionId": sessionId}


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

def close_all_session(user_id:int) -> dict:
    """Cierra todas las sesiones activas de un usuario"""
    value = db.execute_non_query("UPDATE usuariossesiones SET bactivo = FALSE WHERE idusuario = %s", (int(user_id), ))
    sessions = Session.query.filter_by(userId=user_id).all()
    if sessions:
        for session in sessions:
            session.isActive = False
        db.session.commit()
        
    # if value == 0:
    #     return {"sessionId": 0}
    
    return {"sessionId": 0}

