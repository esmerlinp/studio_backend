from ...extensions import db

class PhoneType(db.Model):
    __tablename__ = "tipostelefono"
    __table_args__ = {"schema": "master"}

    id = db.Column("idtipotelefono", db.SmallInteger, primary_key=True)
    name = db.Column("stipotelefono", db.String(50), nullable=False)
    is_active = db.Column("bactivo", db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }
