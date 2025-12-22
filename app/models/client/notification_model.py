from ...extensions import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = "notificaciones"

    id = db.Column("idnotificacion", db.Integer, primary_key=True)
    user_id = db.Column("idusuario", db.Integer, nullable=False, index=True)

    title = db.Column("stitulo", db.String(150), nullable=False)
    message = db.Column("smensaje", db.Text, nullable=False)

    # 👉 CONTEXTO
    resource_type = db.Column("stiporecurso", db.String(50), nullable=True)   # employee
    resource_id = db.Column("idrecurso", db.Integer, nullable=True)        # 123
    action = db.Column("saccion", db.String(50), nullable=True)          # created
    target_url = db.Column("surltarget", db.String(255), nullable=True)     # /employees/123

    read = db.Column("bleida", db.Boolean, default=False, nullable=False)
    created_at = db.Column("dfechacreacion", db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "read": self.read,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "action": self.action,
            "target_url": self.target_url,
            "created_at": self.created_at.isoformat()
        }
