from app import db
from sqlalchemy.dialects.postgresql import NUMERIC

class ChildDiscountView(db.Model):
    __tablename__ = 'vlistadescxhijos'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key - View doesn't have a unique ID, so using composite PK
    childNumber = db.Column("inumhijo", db.Integer, primary_key=True)
    cycleId = db.Column("idciclo", db.Integer, primary_key=True)

    # Columns
    value = db.Column("ivalor", NUMERIC)
    discountType = db.Column("stipodescuento", db.String)
    discountDescription = db.Column("stipodescuentodescripcion", db.String)

    def to_dict(self):
        return {
            "childNumber": self.childNumber,
            "cycleId": self.cycleId,
            "value": float(self.value) if self.value is not None else 0.0,
            "discountType": self.discountType,
            "discountDescription": self.discountDescription
        }
