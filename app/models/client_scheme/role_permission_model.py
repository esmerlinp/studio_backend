from app import db

class RolePermission(db.Model):
    """
    Modelo que representa la tabla 'cliente.rolespermisos'
    """
    __tablename__ = 'rolespermisos'
    __table_args__ = {"schema": "cliente"}

    id = db.Column('idrolpermiso', db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column('idrol', db.Integer, db.ForeignKey('cliente.roles.idrol'), nullable=False)
    screen_functionality_id = db.Column('idpantallafuncionalidad', db.Integer, nullable=False)
    is_allowed = db.Column('bpermitido', db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "role_id": self.role_id,
            "screen_functionality_id": self.screen_functionality_id,
            "is_allowed": self.is_allowed
        }
