from app import db

class Allergy(db.Model):
    __tablename__ = 'alergias'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idalergia', db.SmallInteger, primary_key=True)
    name = db.Column('salergia', db.String(50), nullable=False)
    is_active = db.Column('bactivo', db.Boolean, nullable=False, default=True)

    def __init__(self, id, name, is_active=True):
        self.id = id
        self.name = name
        self.is_active = is_active

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }

    def __repr__(self):
        return f'<Allergy {self.name}>'
