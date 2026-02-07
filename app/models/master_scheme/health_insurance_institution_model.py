from app import db

class HealthInsuranceInstitution(db.Model):
    __tablename__ = 'institucionessegmed'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idinstitucionsegmed', db.SmallInteger, primary_key=True, autoincrement=True)
    name = db.Column('sinstitucionsegmed', db.String(50), nullable=False)
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
        return f'<HealthInsuranceInstitution {self.name}>'
