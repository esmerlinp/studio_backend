from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from app.core import db

from dataclasses import dataclass
from typing import Optional

@dataclass
class UserModel:
    isActive: Optional[bool] = None
    isBlocked: Optional[bool] = None
    mustChangePassword: Optional[bool] = None
    isConfirmedUser: Optional[bool] = None
    tokenExpirationDate: Optional[str] = None
    blockedDate: Optional[str] = None
    lastPasswordChangeDate: Optional[str] = None
    lastLoginDate: Optional[str] = None
    userId: Optional[int] = None
    loginAttempts: Optional[int] = None
    lastName: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    photo: Optional[str] = None
    firstName: Optional[str] = None
    recoveryToken: Optional[str] = None
    username: Optional[str] = None



# def get_user_by_id(user_id) -> UserModel:
#     user = db.fetch_one(
#         "SELECT * FROM usuarios WHERE susuario = %s",
#         (username,)
#     )


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


def get_user_by_id(user_id) -> Optional[UserModel]:
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


# def get_users() -> list[UserModel]:
#     user = db.fetch_one(
#         "SELECT * FROM usuarios WHERE susuario = %s",
#         (username,)
#     )
    