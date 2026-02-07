from app import db
from sqlalchemy.dialects.postgresql import TIMESTAMP, NUMERIC

class TaxListView(db.Model):
    __tablename__ = 'vlistaimpuestos'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idimpuesto", db.Integer, primary_key=True)

    # Columns
    date = db.Column("dfecha", TIMESTAMP)
    percentage = db.Column("nporciento", NUMERIC)
    isActive = db.Column("bactivo", db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "percentage": float(self.percentage) if self.percentage is not None else 0.0,
            "isActive": self.isActive
        }
