from app import db

class Role(db.Model):
    """
    Modelo que representa la tabla 'cliente.roles'
    Contiene la definición de roles y sus permisos programáticos.
    """
    __tablename__ = 'roles'

    # Mapeo de columnas con nombres en inglés
    id = db.Column('idrol', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('srol', db.String(50), nullable=False, unique=True)
    description = db.Column('sdescripcion', db.String(200))
    is_active = db.Column('bactivo', db.Boolean, nullable=False, default=True)
    code = db.Column('scodigo', db.String(20), unique=True)


    def __init__(self, name, code=None, description=None, is_active=True):
        self.name = name
        self.code = code
        self.description = description
        self.is_active = is_active

    def __repr__(self):
        return f"<Role {self.code if self.code else self.name}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "is_active": self.is_active
        }