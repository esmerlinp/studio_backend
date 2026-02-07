from app import db

class PartialListView(db.Model):
    __tablename__ = 'vlistaparciales'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idparcial", db.Integer, primary_key=True)

    # Columns
    name = db.Column("sparcial", db.String)
    shortName = db.Column("sparcialcorto", db.String)
    isActive = db.Column("bactivo", db.Boolean)
    isFormula = db.Column("bformula", db.Boolean)
    formulaId = db.Column("idformula", db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "shortName": self.shortName,
            "isActive": self.isActive,
            "isFormula": self.isFormula,
            "formulaId": self.formulaId
        }
