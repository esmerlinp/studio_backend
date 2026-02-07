from app import db
from sqlalchemy.dialects.postgresql import NUMERIC

class CyclePartialListView(db.Model):
    __tablename__ = 'vlistaparcialesciclos'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idsubcicparcial", db.Integer, primary_key=True)

    # Columns
    subCycleId = db.Column("idsubciclo", db.Integer)
    subCycleName = db.Column("ssubciclo", db.String)
    
    cycleId = db.Column("idciclo", db.Integer)
    cycleName = db.Column("sciclo", db.String)
    
    partialId = db.Column("idparcial", db.Integer)
    partialName = db.Column("sparcial", db.String)
    partialShortName = db.Column("sparcialcorto", db.String)
    
    levelId = db.Column("idnivel", db.Integer)
    levelName = db.Column("snivel", db.String)
    
    minGrade = db.Column("nminimo", NUMERIC)
    maxGrade = db.Column("nmaximo", NUMERIC)
    minPassingGrade = db.Column("nminimoaprueba", NUMERIC)
    
    isFormula = db.Column("bformula", db.Boolean)
    formulaId = db.Column("idformula", db.Integer)
    formula = db.Column("sformula", db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "subCycleId": self.subCycleId,
            "subCycleName": self.subCycleName,
            "cycleId": self.cycleId,
            "cycleName": self.cycleName,
            "partialId": self.partialId,
            "partialName": self.partialName,
            "partialShortName": self.partialShortName,
            "levelId": self.levelId,
            "levelName": self.levelName,
            "minGrade": float(self.minGrade) if self.minGrade is not None else 0.0,
            "maxGrade": float(self.maxGrade) if self.maxGrade is not None else 0.0,
            "minPassingGrade": float(self.minPassingGrade) if self.minPassingGrade is not None else 0.0,
            "isFormula": self.isFormula,
            "formulaId": self.formulaId,
            "formula": self.formula
        }
