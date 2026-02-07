from app import db

class PaymentFrequencyListView(db.Model):
    __tablename__ = 'vlistafrecuenciapagos'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idfrecuenciapago", db.Integer, primary_key=True)

    # Columns
    frequencyName = db.Column("sfrecuenciapago", db.String)
    paymentCount = db.Column("icantpagos", db.Integer)
    isActive = db.Column("bactivo", db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "frequencyName": self.frequencyName,
            "paymentCount": self.paymentCount,
            "isActive": self.isActive
        }
