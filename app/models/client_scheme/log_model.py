from datetime import datetime
from ...extensions import db


class AuditLog(db.Model):
    __tablename__ = "auditoria"


    # -------------------------
    # PK
    # -------------------------
    id = db.Column(
        "idauditoria",
        db.Integer,
        primary_key=True
    )

    # -------------------------
    # Quién
    # -------------------------
    user_id = db.Column(
        "idusuario",
        db.Integer,
        nullable=False,
        index=True
    )

    # -------------------------
    # Qué
    # -------------------------
    action = db.Column(
        "saccion",
        db.String(20),
        nullable=False
    )

    resource_type = db.Column(
        "stiporecurso",
        db.String(50),
        nullable=False
    )

    resource_id = db.Column(
        "idrecurso",
        db.Integer,
        nullable=True,
        index=True
    )

    description = db.Column(
        "sdescripcion",
        db.Text,
        nullable=True
    )

    # -------------------------
    # Desde dónde
    # -------------------------
    ip_address = db.Column(
        "sipdireccion",
        db.String(45),
        nullable=True
    )

    user_agent = db.Column(
        "suseragent",
        db.String(255),
        nullable=True
    )

    # -------------------------
    # Valores
    # -------------------------
    old_values = db.Column(
        "jvaloresant",
        db.JSON,
        nullable=True
    )

    new_values = db.Column(
        "jvaloresnue",
        db.JSON,
        nullable=True
    )
    
    #Clasificación de la operación: DML (Cambios), ERROR, WARNING o Eventos de Sesión
    accion_type = db.Column(
        "stipoaccion",
        db.String(20),
        nullable=False,
        default="DML"
    )

    # -------------------------
    # Cuándo
    # -------------------------
    created_at = db.Column(
        "dfechacreacion",
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # -------------------------
    # Utilidad
    # -------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "accion_type": self.accion_type,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "description": self.description,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return (
            f"<AuditLog id={self.id} action={self.action} "
            f"resource={self.resource_type} user={self.user_id}>"
        )
