from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Module(db.Model):
    __tablename__ = 'modulos'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idmodulo', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('smodulo', db.String(50), nullable=False, unique=True)
    description = db.Column('sdescripcion', db.String(500))
    icon = db.Column('sicono', db.String(100))
    order = db.Column('iorden', db.Integer)
    is_active = db.Column('bactivo', db.Boolean, nullable=False, default=True)
    uuid = db.Column('uuidmodulo', UUID(as_uuid=True), nullable=False, default=uuid.uuid4)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "order": self.order,
            "is_active": self.is_active,
            "uuid": str(self.uuid)
        }
