from ...extensions import db

class BloodType(db.Model):
    __tablename__ = "tipossangre"
    __table_args__ = {"schema": "master"}

    id = db.Column("idtiposangre", db.SmallInteger, primary_key=True)
    name = db.Column("stiposangre", db.String(50), nullable=False)
    is_active = db.Column("bactivo", db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }
