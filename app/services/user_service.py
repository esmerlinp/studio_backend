
from app.models.user_model import User
from typing import Optional, List
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
    


