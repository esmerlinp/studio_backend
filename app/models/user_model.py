from dataclasses import dataclass
from typing import Optional
from app.database import db

from dataclasses import dataclass
from typing import Optional
from flask_jwt_extended import  get_jwt_identity
from flask import request

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


