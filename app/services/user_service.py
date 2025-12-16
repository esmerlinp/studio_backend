
from app.models.user_model import User
from typing import Optional, List
from app.database import db
from flask import request
from werkzeug.security import  generate_password_hash
from ..extensions import db as sqlalchemy_db

def get_user_by_user_name_with_passwd(user_name) -> Optional[User]:
    user = User.query.filter_by(username=user_name).first()
    return user



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
    


