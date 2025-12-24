from datetime import datetime
from app import db

class UserRole(db.Model):
    __tablename__ = "usuariosroles"

    id = db.Column("idusuariorol", db.Integer, primary_key=True)
    user_id = db.Column("idusuario", db.Integer, nullable=False, index=True)
    role_id = db.Column("idrol", db.Integer, nullable=False, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "role_id": self.role_id
        }
