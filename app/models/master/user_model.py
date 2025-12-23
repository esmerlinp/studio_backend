
from ...extensions import db
from app.models.master.user_roles import UserRole
from app.models.master.roles_model import Role

class User(db.Model):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "master"}
    
    userId = db.Column('idusuario', db.Integer, primary_key=True)
    username = db.Column('susuario', db.String(50), nullable=False)
    firstName = db.Column('snombres',  db.String(100), nullable=False)
    lastName = db.Column('sapellidos', db.String(100), nullable=False)
    email = db.Column("scorreoelectronico", db.String(100), nullable=False)
    uuid = db.Column("uuidcliente", db.String(100), nullable=False)
    photo = db.Column("sfoto", db.String(500), nullable=True)
    isActive = db.Column("bactivo", db.Boolean)
    isConfirmedUser = db.Column("busuarioconfirmado", db.Boolean)
    mustChangePassword = db.Column("bcambiarcontrasena", db.Boolean)
    loginAttempts = db.Column("iintentoslogin",  db.Integer, nullable=False, default=0)
    isBlocked = db.Column("bbloqueado", db.Boolean)
    blockedDate = db.Column("dfechabloqueo", db.DateTime, nullable=True)
    lastLoginDate = db.Column("dultimologin", db.DateTime, nullable=True)
    recoveryToken = db.Column("stokenrecuperacion", db.String(100), nullable=True)
    tokenExpirationDate = db.Column("dexpiraciontoken", db.DateTime, nullable=True)
    lastPasswordChangeDate = db.Column("dfechaultcambiocont",db.DateTime, nullable=False)
    password = db.Column("scontrasena", db.String(500), nullable=False)
    
    # preferences = db.relationship(
    #     "UserPreference",
    #     uselist=False,
    #     backref="user",
    #     cascade="all, delete"
    # )
    

    def to_dict(self, include_sensitive=False):
        data = {
            "userId": self.userId,
            "username": self.username,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "photo": self.photo,
            "isActive": self.isActive,
            "isConfirmedUser": self.isConfirmedUser,
            "mustChangePassword": self.mustChangePassword,
            "loginAttempts": self.loginAttempts,
            "isBlocked": self.isBlocked,
            "blockedDate": self.blockedDate.isoformat() if self.blockedDate else None,
            "lastLoginDate": self.lastLoginDate.isoformat() if self.lastLoginDate else None,
            "tokenExpirationDate": self.tokenExpirationDate.isoformat() if self.tokenExpirationDate else None,
            "lastPasswordChangeDate": self.lastPasswordChangeDate.isoformat() if self.lastPasswordChangeDate else None
        }
        if include_sensitive:
            data["recoveryToken"] = self.recoveryToken
            data["password"] = self.password
        return data