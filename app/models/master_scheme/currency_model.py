from app import db

class Currency(db.Model):
    __tablename__ = 'monedas'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idmoneda', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('smoneda', db.String(50), nullable=False)
    iso_code = db.Column('smoneda3', db.String(3), nullable=False, unique=True)
    is_active = db.Column('bactivo', db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "iso_code": self.iso_code,
            "is_active": self.is_active
        }
