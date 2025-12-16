
from app.models.user_model import UserModel, User
from typing import Optional, List
from app.database import db
from flask import request
from werkzeug.security import  generate_password_hash
from ..extensions import db as sqlalchemy_db

def get_user_by_user_name_with_passwd(user_name) -> Optional[User]:
    user = User.query.filter_by(username=user_name).first()
    return user
    # user = db.fetch_one(
    #     "SELECT * FROM usuarios WHERE susuario = %s",
    #     (user_name,)
    # )
    
    # if not user:
    #     return None

    # return UserModel(
    #     isActive=user.get("bactivo"),
    #     isBlocked=user.get("bbloqueado"),
    #     mustChangePassword=user.get("bcambiarcontrasena"),
    #     isConfirmedUser=user.get("busuarioconfirmado"),
    #     tokenExpirationDate=user.get("dexpiraciontoken"),
    #     blockedDate=user.get("dfechabloqueo"),
    #     lastPasswordChangeDate=user.get("dfechaultcambiocont"),
    #     lastLoginDate=user.get("dultimologin"),
    #     userId=user.get("idusuario"),
    #     loginAttempts=user.get("iintentoslogin"),
    #     lastName=user.get("sapellidos"),
    #     password=user.get("scontrasena"),
    #     email=user.get("scorreoelectronico"),
    #     photo=user.get("sfoto"),
    #     firstName=user.get("snombres"),
    #     recoveryToken=user.get("stokenrecuperacion"),
    #     username=user.get("susuario")
    # )


def change_user_password(user_id:int, new_password:int, sessionId=None) -> Optional[User]:
    password_hashed = generate_password_hash(password=new_password)
    
    user = User.query.filter_by(userId=user_id).first()
    if not user:
        return None 
    
    user.password = password_hashed
    sqlalchemy_db.session.commit()
    return user
    
    # value = db.execute_non_query("UPDATE usuarios SET scontrasena = %s WHERE idusuario = %s", (password_hashed, user_id, ))
    # if value == 0:
    #     return None
    # #forzar cierre de sesiones abiertas excepto la actual
    # if sessionId:
    #     close_all_session_except_current(sessionId=sessionId, user_id=user_id)
    
    
    # return get_user_by_id(user_id=user_id)




def get_user_by_user_name(user_name) -> Optional[User]:
    user = User.query.filter_by(username=user_name).first()
    return user


def get_user_by_email(email) -> Optional[User]:
    user = User.query.filter_by(email=email).first()
    return user


def get_user_by_id(user_id:int) -> Optional[User]:
    user = User.query.filter_by(userId=user_id).first()
    return user
    




def get_all_users() -> List[User]:
    users = User.query.all()        
    return users
    



def get_open_sessions(user_id: int) -> List[dict]:
    rows = db.fetch_data("SELECT * FROM usuariossesiones where bactivo = TRUE AND idusuario = %s", (int(user_id), ))

 
    sessions = []
    for s in rows:
        sessions.append(
            {
                "sessionId": s.get("idusuariosesion", 0),
                "lastAccess": s.get("dultimoacceso", None),
                "expired": s.get("dfechaexpiracion", None),
                "device": f"Random device {s.get("idusuariosesion", 0)}",
                "deviceIp": request.remote_addr #TODO: sustituir por campo real cuando se implemente
            }
        )

    return sessions

def close_session(sessionId, user_id:int) -> dict:
    value = db.execute_non_query("UPDATE usuariossesiones SET bactivo = FALSE WHERE idusuariosesion = %s AND idusuario = %s", (sessionId, int(user_id), ))
    if value == 0:
        return {"sessionId": 0}
    
    return {"sessionId": sessionId}

def close_all_session_except_current(sessionId, user_id:int) -> dict:
    """Cierra todas las sesiones activas de un usuario excepto la actual"""
    value = db.execute_non_query("UPDATE usuariossesiones SET bactivo = FALSE WHERE idusuariosesion <> %s AND idusuario = %s", (sessionId, int(user_id), ))
    if value == 0:
        return {"sessionId": 0}
    
    return {"sessionId": sessionId}

def close_all_session(user_id:int) -> dict:
    """Cierra todas las sesiones activas de un usuario"""
    value = db.execute_non_query("UPDATE usuariossesiones SET bactivo = FALSE WHERE idusuario = %s", (int(user_id), ))
    if value == 0:
        return {"sessionId": 0}
    
    return {"sessionId": value}

