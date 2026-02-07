from app import db

class SubCycleCourseCompetencyView(db.Model):
    __tablename__ = 'vsubciccompetenciascurso'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idsubciccompetenciacurso", db.Integer, primary_key=True)

    # Columns
    subCycleId = db.Column("idsubciclo", db.Integer)
    subCycleName = db.Column("ssubciclo", db.String)
    
    courseId = db.Column("idcurso", db.Integer)
    courseName = db.Column("scurso", db.String)
    
    competencyId = db.Column("idcompetencia", db.Integer)
    competencyName = db.Column("scompetencia", db.String)
    competencyDescription = db.Column("scompetenciadescripcion", db.String)
    
    cycleId = db.Column("idciclo", db.Integer)
    
    subjectId = db.Column("idasignatura", db.Integer)
    subjectName = db.Column("sasignatura", db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "subCycleId": self.subCycleId,
            "subCycleName": self.subCycleName,
            "courseId": self.courseId,
            "courseName": self.courseName,
            "competencyId": self.competencyId,
            "competencyName": self.competencyName,
            "competencyDescription": self.competencyDescription,
            "cycleId": self.cycleId,
            "subjectId": self.subjectId,
            "subjectName": self.subjectName
        }
