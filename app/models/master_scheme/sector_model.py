from app import db

class Sector(db.Model):
    __tablename__ = 'sectores'
    __table_args__ = {'schema': 'master'}

    # Propiedad en inglés = Column('nombre_real_en_db', tipo, ...)
    id = db.Column('idsector', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('ssector', db.String(50), nullable=False)
    city_id = db.Column('idciudad', db.Integer, db.ForeignKey('master.ciudades.idciudad'), nullable=False)
    is_active = db.Column('bactivo', db.Boolean, nullable=False, default=True)

    # Relaciones
    # backref 'city' ya viene implícito si se configuró en el modelo City
    #clients = db.relationship('Client', backref='billing_sector', lazy=True)

    def __init__(self, name, city_id, is_active=True):
        self.name = name
        self.city_id = city_id
        self.is_active = is_active

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city_id": self.city_id,
            "is_active": self.is_active
        }

    def __repr__(self):
        return f'<Sector {self.name} (City ID: {self.city_id})>'