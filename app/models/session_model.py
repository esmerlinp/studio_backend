
from ..extensions import db

class Session(db.Model):
    __tablename__ = "usuariossesiones"
    
    sessionId = db.Column('idusuariosesion', db.Integer, primary_key=True)
    userId = db.Column('idusuario', db.Integer, nullable=False)
    refreshToken = db.Column('srefreshtoken', db.String(500), nullable=False)
    expirationDate = db.Column('dfechaexpiracion', db.DateTime, nullable=False)
    lastAccessDate = db.Column('dultimoacceso', db.DateTime, nullable=False)
    isActive = db.Column('bactivo', db.Boolean, nullable=False, default=True)
    
    def to_dict(self, include_sensitive=False):
        data = {
            "sessionId": self.sessionId,
            "userId": self.userId,
            "expirationDate": self.expirationDate.isoformat() if self.expirationDate else None,
            "lastAccessDate": self.lastAccessDate.isoformat() if self.lastAccessDate else None,
            "isActive": self.isActive
        }
        if include_sensitive:
            data["refreshToken"] = self.refreshToken
            
        return data