
from app.models.user_model import UserModel
from typing import Optional
from app.database import db
from flask import request

def get_user_by_user_name_with_passwd(user_name) -> Optional[UserModel]:
    user = db.fetch_one(
        "SELECT * FROM usuarios WHERE susuario = %s",
        (user_name,)
    )
    
    if not user:
        return None

    return UserModel(
        isActive=user.get("bactivo"),
        isBlocked=user.get("bbloqueado"),
        mustChangePassword=user.get("bcambiarcontrasena"),
        isConfirmedUser=user.get("busuarioconfirmado"),
        tokenExpirationDate=user.get("dexpiraciontoken"),
        blockedDate=user.get("dfechabloqueo"),
        lastPasswordChangeDate=user.get("dfechaultcambiocont"),
        lastLoginDate=user.get("dultimologin"),
        userId=user.get("idusuario"),
        loginAttempts=user.get("iintentoslogin"),
        lastName=user.get("sapellidos"),
        password=user.get("scontrasena"),
        email=user.get("scorreoelectronico"),
        photo=user.get("sfoto"),
        firstName=user.get("snombres"),
        recoveryToken=user.get("stokenrecuperacion"),
        username=user.get("susuario")
    )



def get_user_by_user_name(user_name) -> Optional[UserModel]:
    user = db.fetch_one(
        "SELECT * FROM usuarios WHERE susuario = %s",
        (user_name,)
    )
    
    if not user:
        return None

    return UserModel(
        isActive=user.get("bactivo"),
        isBlocked=user.get("bbloqueado"),
        mustChangePassword=user.get("bcambiarcontrasena"),
        isConfirmedUser=user.get("busuarioconfirmado"),
        tokenExpirationDate=user.get("dexpiraciontoken"),
        blockedDate=user.get("dfechabloqueo"),
        lastPasswordChangeDate=user.get("dfechaultcambiocont"),
        lastLoginDate=user.get("dultimologin"),
        userId=user.get("idusuario"),
        loginAttempts=user.get("iintentoslogin"),
        lastName=user.get("sapellidos"),
        email=user.get("scorreoelectronico"),
        photo=user.get("sfoto"),
        firstName=user.get("snombres"),
        recoveryToken=user.get("stokenrecuperacion"),
        username=user.get("susuario")
    )


def get_user_by_id(user_id:int) -> Optional[UserModel]:
    user = db.fetch_one(
        "SELECT * FROM usuarios WHERE idusuario = %s",
        (user_id,)
    )
    
    if not user:
        return None

    return UserModel(
        isActive=user.get("bactivo"),
        isBlocked=user.get("bbloqueado"),
        mustChangePassword=user.get("bcambiarcontrasena"),
        isConfirmedUser=user.get("busuarioconfirmado"),
        tokenExpirationDate=user.get("dexpiraciontoken"),
        blockedDate=user.get("dfechabloqueo"),
        lastPasswordChangeDate=user.get("dfechaultcambiocont"),
        lastLoginDate=user.get("dultimologin"),
        userId=user.get("idusuario"),
        loginAttempts=user.get("iintentoslogin"),
        lastName=user.get("sapellidos"),
        email=user.get("scorreoelectronico"),
        photo=user.get("sfoto"),
        firstName=user.get("snombres"),
        recoveryToken=user.get("stokenrecuperacion"),
        username=user.get("susuario")
    )

    


from typing import List

def get_all_users() -> List[UserModel]:
    rows = db.fetch_data("SELECT * FROM usuarios")

    users: List[UserModel] = []

    for user in rows:
        users.append(
            UserModel(
                isActive=user.get("bactivo"),
                isBlocked=user.get("bbloqueado"),
                mustChangePassword=user.get("bcambiarcontrasena"),
                isConfirmedUser=user.get("busuarioconfirmado"),
                tokenExpirationDate=user.get("dexpiraciontoken"),
                blockedDate=user.get("dfechabloqueo"),
                lastPasswordChangeDate=user.get("dfechaultcambiocont"),
                lastLoginDate=user.get("dultimologin"),
                userId=user.get("idusuario"),
                loginAttempts=user.get("iintentoslogin"),
                lastName=user.get("sapellidos"),
                email=user.get("scorreoelectronico"),
                photo=user.get("sfoto"),
                firstName=user.get("snombres"),
                recoveryToken=user.get("stokenrecuperacion"),
                username=user.get("susuario")
            )
        )

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

