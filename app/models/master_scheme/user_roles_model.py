from ...extensions import db


class UserRole(db.Model):
    __tablename__ = "usuariosroles"
    __table_args__ = (
        db.UniqueConstraint("idusuario", "idrol", name="uq_usuariosroles_usuario_rol"),
        {"schema": "master"}
    )

    id = db.Column(
        "idusuariorol",
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        "idusuario",
        db.Integer,
        db.ForeignKey("master.usuarios.idusuario", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    role_id = db.Column(
        "idrol",
        db.Integer,
        db.ForeignKey("master.roles.idrol", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # role = db.relationship(
    #     "Role",
    #     back_populates="users"
    # )


    # ───────────────────────────────────────
    # Utilidades
    # ───────────────────────────────────────
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "role_id": self.role_id,
            # "role_code": self.role.code if self.role else None
        }

    def __repr__(self):
        return (
            f"<UserRole id={self.id} "
            f"user_id={self.user_id} "
            f"role_id={self.role_id}>"
        )
