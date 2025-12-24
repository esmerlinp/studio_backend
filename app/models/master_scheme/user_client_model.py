from ...extensions import db
from sqlalchemy.dialects.postgresql import UUID


class UsuarioCliente(db.Model):
    __tablename__ = "usuariosclientes"
    __table_args__ = {"schema": "master"}

    id = db.Column(
        "idusuariocliente",
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        "idusuario",
        db.Integer,
        db.ForeignKey("master.usuarios.idusuario"),
        nullable=False,
        index=True
    )

    client_uuid = db.Column(
        "uuidcliente",
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )

    # ───────────────────────────────────────
    # Relaciones (opcional pero recomendado)
    # ───────────────────────────────────────
    user = db.relationship(
        "User",
        backref=db.backref("clientes", lazy="dynamic")
    )

    # ───────────────────────────────────────
    # Utilidades
    # ───────────────────────────────────────
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "client_uuid": str(self.client_uuid)
        }

    def __repr__(self):
        return (
            f"<UsuarioCliente id={self.id} "
            f"user_id={self.user_id} "
            f"client_uuid={self.client_uuid}>"
        )
