from ...extensions import db

class PaymentProcessor(db.Model):
    __tablename__ = "procesadorespagos"
    __table_args__ = {"schema": "master"}

    id = db.Column("idprocesadorpago", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("sprocesadorpago", db.String(50), nullable=False)
    is_active = db.Column("bactivo", db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }
