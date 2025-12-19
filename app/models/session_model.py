
from ..extensions import db
import datetime
class Session(db.Model):
    __tablename__ = "usuariossesiones"
    __table_args__ = {"schema": "master"}
    
    sessionId = db.Column('idusuariosesion', db.Integer, primary_key=True, comment="Id de la session")
    userId = db.Column('idusuario', db.Integer, nullable=False, comment="Id del usuario")
    refreshToken = db.Column('srefreshtoken', db.String(500), nullable=False)
    expirationDate = db.Column('dfechaexpiracion',db.DateTime(timezone=True), nullable=False)
    lastAccessDate = db.Column('dultimoacceso', db.DateTime(timezone=True), nullable=False)
    isActive = db.Column('bactivo', db.Boolean, nullable=False, default=True)
    ipAddress = db.Column('sdireccionip', db.String(45), nullable=False)
    userAgent = db.Column('sinfonav', db.String(500), nullable=True, comment="Información del navegador/dispositivo")
    
    deviceInfo = db.Column('sinfodispositivo',db.String(200), nullable=True) #device_info: Datos resumidos de dispositivo (ej. móvil/desktop).
    
    latitude = db.Column('nlatitud', db.Float, nullable=True)
    longitude = db.Column('nlongitud',db.Float, nullable=True)
    
    createAt = db.Column('dfechainicio', db.DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow())
    closeAt = db.Column('dfechafin', db.DateTime(timezone=True), nullable=True)
    
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
    
