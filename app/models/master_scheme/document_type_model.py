from ...extensions import db

class DocumentType(db.Model):
    __tablename__ = "tiposdocumento"
    __table_args__ = {"schema": "master"}

    id = db.Column("idtipodocumento", db.SmallInteger, primary_key=True)
    name = db.Column("stipodocumento", db.String(50), nullable=False)
    is_active = db.Column("bactivo", db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }
