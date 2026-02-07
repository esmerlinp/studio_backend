from ...extensions import db

class RolePermission(db.Model):
    __tablename__ = "rolespermisos"
    __table_args__ = (
        db.UniqueConstraint("idrol", "idpantallafuncionalidad", name="uq_rolespermisos_rol_pantallafunc"),
        {"schema": "master"}
    )

    id = db.Column("idrolpermiso", db.Integer, primary_key=True)
    role_id = db.Column("idrol", db.Integer, db.ForeignKey("master.roles.idrol", ondelete="CASCADE"), nullable=False)
    screen_functionality_id = db.Column("idpantallafuncionalidad", db.Integer, db.ForeignKey("master.pantallasfuncionalidades.idpantallafuncionalidad", ondelete="CASCADE"), nullable=False)
    is_allowed = db.Column("bpermitido", db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "role_id": self.role_id,
            "screen_functionality_id": self.screen_functionality_id,
            "is_allowed": self.is_allowed
        }
