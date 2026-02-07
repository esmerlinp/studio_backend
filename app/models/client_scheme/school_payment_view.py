from app import db
from sqlalchemy.dialects.postgresql import NUMERIC, TIMESTAMP

class SchoolPaymentView(db.Model):
    __tablename__ = 'vpagoescolaridad'
    __table_args__ = {'info': dict(is_view=True)}

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
            "observation": self.observation
        }
