from app import db
from sqlalchemy.dialects.postgresql import NUMERIC, TIMESTAMP

class SchoolPaymentView(db.Model):
    __tablename__ = 'vpagoescolaridad'
    __table_args__ = {'schema': 'cliente', 'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idpago", db.Integer, primary_key=True)

    # Columns
    paymentDate = db.Column("dfechapago", TIMESTAMP)
    amount = db.Column("nmonto", NUMERIC)
    
    studentId = db.Column("idestudiante", db.Integer)
    studentName = db.Column("snombreresponsable", db.String)
    
    cycleId = db.Column("idciclo", db.Integer)
    cycleName = db.Column("sciclo", db.String)
    
    conceptId = db.Column("idconcepto", db.Integer)
    conceptName = db.Column("sconcepto", db.String)
    
    paymentMethod = db.Column("sfpago", db.String)
    observation = db.Column("scomentario", db.String)
    
    # Financial details
    discount = db.Column("ndescuento", NUMERIC)
    surcharge = db.Column("nrecargo", NUMERIC)
    tax = db.Column("nitbis", NUMERIC)
    subtotal = db.Column("nsubtotal", NUMERIC)
    quota = db.Column("icuota", db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "paymentDate": self.paymentDate.isoformat() if self.paymentDate else None,
            "amount": float(self.amount) if self.amount is not None else 0.0,
            "studentId": self.studentId,
            "studentName": self.studentName,
            "cycleId": self.cycleId,
            "cycleName": self.cycleName,
            "conceptId": self.conceptId,
            "conceptName": self.conceptName,
            "paymentMethod": self.paymentMethod,
            "observation": self.observation,
            "discount": float(self.discount) if self.discount is not None else 0.0,
            "surcharge": float(self.surcharge) if self.surcharge is not None else 0.0,
            "tax": float(self.tax) if self.tax is not None else 0.0,
            "subtotal": float(self.subtotal) if self.subtotal is not None else 0.0,
            "quota": self.quota
        }
