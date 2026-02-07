from app import db

class ActiveCycleCompetencyView(db.Model):
    __tablename__ = 'vcompetenciascicloactivo'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idsubciccompetenciacurso", db.Integer, primary_key=True)

    # Columns
    subCycleId = db.Column("idsubciclo", db.Integer)
    subCycleName = db.Column("ssubciclo", db.String)
    subCycleOrder = db.Column("iordensubcic", db.Integer)
    
    competencyId = db.Column("idcompetencia", db.Integer)
    competencyName = db.Column("scompetencia", db.String)
    
    courseId = db.Column("idcurso", db.Integer)
    courseName = db.Column("scurso", db.String)
    
    levelId = db.Column("idnivel", db.Integer)
    levelName = db.Column("snivel", db.String)
    
    periods = db.Column("iperiodos", db.Integer)
    allowsRecovery = db.Column("bpermiterecuperacion", db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "subCycleId": self.subCycleId,
            "subCycleName": self.subCycleName,
            "subCycleOrder": self.subCycleOrder,
            "competencyId": self.competencyId,
            "competencyName": self.competencyName,
            "courseId": self.courseId,
            "courseName": self.courseName,
            "levelId": self.levelId,
            "levelName": self.levelName,
            "periods": self.periods,
            "allowsRecovery": self.allowsRecovery
        }
