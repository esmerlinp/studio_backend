from ...extensions import db

class AttendanceType(db.Model):
    __tablename__ = "tiposasistencia"
    __table_args__ = {"schema": "master"}

    id = db.Column("idtipoasistencia", db.SmallInteger, primary_key=True, autoincrement=True)
    name = db.Column("stipoasistencia", db.String(50), nullable=False)
    is_active = db.Column("bactivo", db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }
