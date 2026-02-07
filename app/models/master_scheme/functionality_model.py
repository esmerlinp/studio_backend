from app import db
import uuid

class Functionality(db.Model):
    __tablename__ = 'funcionalidades'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idfuncionalidad', db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column('uuidfuncionalidad', db.UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    name = db.Column('sfuncionalidad', db.String(50), nullable=False)
    description = db.Column('sdescripcion', db.String(200))
    code = db.Column('scodigo', db.String(50))
    is_active = db.Column('bactivo', db.Boolean, nullable=False, default=True)

    def __init__(self, name, description=None, code=None, is_active=True):
        self.name = name
        self.description = description
        self.code = code
        self.is_active = is_active

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": str(self.uuid),
            "name": self.name,
            "description": self.description,
            "code": self.code,
            "is_active": self.is_active
        }

    def __repr__(self):
        return f'<Functionality {self.name}>'
