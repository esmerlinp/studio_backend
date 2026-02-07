from app import db

class FormulaListView(db.Model):
    __tablename__ = 'vlistaformulas'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idformula", db.Integer, primary_key=True)

    # Columns
    description = db.Column("sdescformula", db.String)
    formula = db.Column("sformula", db.String)
    isActive = db.Column("bactivo", db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "formula": self.formula,
            "isActive": self.isActive
        }
