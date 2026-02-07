from app import db
from sqlalchemy.dialects.postgresql import NUMERIC

class SurchargePerDayListView(db.Model):
    __tablename__ = 'vlistarecxdias'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idrecxdia", db.Integer, primary_key=True)

    # Columns
    cycleId = db.Column("idciclo", db.Integer)
    days = db.Column("idias", db.Integer)
    value = db.Column("nvalor", NUMERIC)
    type = db.Column("stipo", db.String)
    typeDescription = db.Column("stipodescripcion", db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "cycleId": self.cycleId,
            "days": self.days,
            "value": float(self.value) if self.value is not None else 0.0,
            "type": self.type,
            "typeDescription": self.typeDescription
        }
