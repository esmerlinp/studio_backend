from app import db

class MedicalInstitution(db.Model):
    __tablename__ = 'institucionesmedicas'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idinstitucionmedica', db.SmallInteger, primary_key=True, autoincrement=True)
    name = db.Column('sinstitucionmedica', db.String(50), nullable=False)
    is_active = db.Column('bactivo', db.Boolean, nullable=False, default=True)

    def __init__(self, name, is_active=True):
        self.name = name
        self.is_active = is_active

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }

    def __repr__(self):
        return f'<MedicalInstitution {self.name}>'
