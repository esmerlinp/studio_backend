from app import db

class PaymentCalendarListView(db.Model):
    __tablename__ = 'vlistacalendariopagos'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idcalendariopago", db.Integer, primary_key=True)

    # Columns
    cycleId = db.Column("idciclo", db.Integer)
    cycleName = db.Column("sciclo", db.String)
    
    paymentFrequencyId = db.Column("idfrecuenciapago", db.Integer)
    paymentFrequencyName = db.Column("sfrecuenciapago", db.String)
    
    quotaNumber = db.Column("inumerocuota", db.Integer)
    monthName = db.Column("snombremes", db.String)
    
    paymentDate = db.Column("dfechapago", db.Date)
    discountDate = db.Column("dfechadescpp", db.Date)
    surchargeDate = db.Column("dfecharec", db.Date)
    
    isCycleActive = db.Column("bciclo_activo", db.Boolean)
    paymentCount = db.Column("icantpagos", db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "cycleId": self.cycleId,
            "cycleName": self.cycleName,
            "paymentFrequencyId": self.paymentFrequencyId,
            "paymentFrequencyName": self.paymentFrequencyName,
            "quotaNumber": self.quotaNumber,
            "monthName": self.monthName,
            "paymentDate": self.paymentDate.isoformat() if self.paymentDate else None,
            "discountDate": self.discountDate.isoformat() if self.discountDate else None,
            "surchargeDate": self.surchargeDate.isoformat() if self.surchargeDate else None,
            "isCycleActive": self.isCycleActive,
            "paymentCount": self.paymentCount
        }
