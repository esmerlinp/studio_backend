from app import db

class Function(db.Model):
    __tablename__ = 'funciones'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idfuncion', db.SmallInteger, primary_key=True, autoincrement=True)
    name = db.Column('sfuncion', db.String(50), nullable=False)
    description = db.Column('sdescfuncion', db.String(500), nullable=False)
    example = db.Column('sejemplofuncion', db.String(500), nullable=False)
    is_active = db.Column('bactivo', db.Boolean, nullable=False, default=True)

    def __init__(self, name, description, example, is_active=True):
        self.name = name
        self.description = description
        self.example = example
        self.is_active = is_active

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "example": self.example,
            "is_active": self.is_active
        }

    def __repr__(self):
        return f'<Function {self.name}>'
