from ...extensions import db

class Gender(db.Model):
    __tablename__ = "sexos"
    __table_args__ = {"schema": "master"}

    id = db.Column("idsexo", db.Integer, primary_key=True)
    name = db.Column("ssexo", db.String(20), nullable=False)
    is_active = db.Column("bactivo", db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }
