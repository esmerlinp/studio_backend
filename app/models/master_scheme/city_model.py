from app import db

class City(db.Model):
    __tablename__ = 'ciudades'
    __table_args__ = {'schema': 'master'}

    # Propiedad en inglés = Column('nombre_real_en_db', tipo, ...)
    id = db.Column('idciudad', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('sciudad', db.String(50), nullable=False)
    country_id = db.Column('idpais', db.Integer, db.ForeignKey('master.paises.idpais'), nullable=False)
    is_active = db.Column('bactivo', db.Boolean, nullable=False, default=True)

    # Relaciones
    # Nota: El backref 'country' ya fue definido en el modelo Country, 
    # lo que permite hacer city.country para obtener el objeto Pais.
    #clients = db.relationship('Client', backref='billing_city', lazy=True)
    #sectors = db.relationship('Sector', backref='city', lazy=True)

    def __init__(self, name, country_id, is_active=True):
        self.name = name
        self.country_id = country_id
        self.is_active = is_active

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country_id": self.country_id,
            "is_active": self.is_active
        }

    def __repr__(self):
        return f'<City {self.name} (Country ID: {self.country_id})>'