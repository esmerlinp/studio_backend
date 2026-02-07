from ...extensions import db

class Profession(db.Model):
    __tablename__ = "profesiones"
    __table_args__ = {"schema": "master"}

    id = db.Column("idprofesion", db.SmallInteger, primary_key=True)
    name = db.Column("sprofesion", db.String(50), nullable=False)
    is_active = db.Column("bactivo", db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }
