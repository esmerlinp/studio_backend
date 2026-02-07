from app import db

class OtherSchool(db.Model):
    __tablename__ = 'otroscolegios'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idotrocolegio', db.Integer, primary_key=True)
    name = db.Column('sotrocolegio', db.String(50), nullable=False)
    is_active = db.Column('bactivo', db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }
