from ...extensions import db
import uuid

class Screen(db.Model):
    __tablename__ = "pantallas"
    __table_args__ = {"schema": "master"}

    id = db.Column("idpantalla", db.Integer, primary_key=True)
    uuid = db.Column("uuidpantalla", db.UUID, nullable=False, unique=True, default=uuid.uuid4)
    module_id = db.Column("idmodulo", db.Integer, db.ForeignKey("master.modulos.idmodulo"), nullable=False)
    name = db.Column("spantalla", db.String(100), nullable=False)
    description = db.Column("sdescripcion", db.String(200))
    route = db.Column("sruta", db.String(200))
    icon = db.Column("sicono", db.String(50))
    order = db.Column("iorden", db.SmallInteger)
    is_active = db.Column("bactivo", db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": str(self.uuid),
            "module_id": self.module_id,
            "name": self.name,
            "description": self.description,
            "route": self.route,
            "icon": self.icon,
            "order": self.order,
            "is_active": self.is_active
        }
