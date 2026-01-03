from app import db 

class Country(db.Model):
    __tablename__ = 'paises'
    __table_args__ = {'schema': 'master'}

    # Propiedad en inglés = Column('nombre_real_en_db', tipo, ...)
    id = db.Column('idpais', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('spais', db.String(50), nullable=False)
    iso_code = db.Column('spais3', db.String(3), nullable=False)
    is_active = db.Column('bactivo', db.Boolean, nullable=False, default=True)

    # Relaciones (Usando nombres en inglés para el acceso en Python)
    #cities = db.relationship('City', backref='country', lazy=True)
    #cities = db.relationship('City', backref='country', lazy=True)
    #clients = db.relationship('Client', backref='billing_country', lazy=True)

    def __init__(self, name, iso_code, is_active=True):
        self.name = name
        self.iso_code = iso_code
        self.is_active = is_active

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "iso_code": self.iso_code,
            "is_active": self.is_active
        }

    def __repr__(self):
        return f'<Country {self.name} ({self.iso_code})>'