from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone
from ...extensions import db

class UserPreference(db.Model):
    __tablename__ = "usuariospreferencias"
    __table_args__ = {"schema": "master"}

    id = db.Column("idusuariopreferencia", db.Integer, primary_key=True)

    userId = db.Column(
        "idusuario",
        db.Integer,
        #db.ForeignKey("usuarios.idusuario", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    preferences = db.Column("jpreferencias", JSONB, nullable=False)

    updatedAt = db.Column(
        "dfechaactualizacion",
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    
    def to_dict(self, include_sensitive=False):
        data = {
            "id": self.id,
            "userId": self.userId,
            "preferences": self.preferences,
            "updatedAt": self.updatedAt,
        }
        # if include_sensitive:
        #     data["recoveryToken"] = self.recoveryToken
        #     data["password"] = self.password
        return data