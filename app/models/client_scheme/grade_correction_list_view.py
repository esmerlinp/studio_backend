from app import db
from sqlalchemy.dialects.postgresql import TIMESTAMP, NUMERIC

class GradeCorrectionListView(db.Model):
    __tablename__ = 'vlistanotascorrecciones'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idnotacorreccion", db.Integer, primary_key=True)

    # Columns
    gradeId = db.Column("idnota", db.Integer)
    
    cycleId = db.Column("idciclo", db.Integer)
    cycleName = db.Column("sciclo", db.String)
    
    subCycleId = db.Column("idsubciclo", db.Integer)
    subCycleName = db.Column("ssubciclo", db.String)
    
    courseId = db.Column("idcurso", db.Integer)
    courseName = db.Column("scurso", db.String)
    
    classroomId = db.Column("idaula", db.Integer)
    classroomName = db.Column("saula", db.String)
    courseClassroom = db.Column("scursoaula", db.String)
    
    studentId = db.Column("idestudiante", db.Integer)
    studentCode = db.Column("scodigoestudiante", db.String)
    studentName = db.Column("sestudiante", db.String)
    
    subjectId = db.Column("idasignatura", db.Integer)
    subjectName = db.Column("sasignatura", db.String)
    
    subjectAreaId = db.Column("idareatematica", db.Integer)
    subjectAreaName = db.Column("sareatematica", db.String)
    
    partialId = db.Column("idparcial", db.Integer)
    partialName = db.Column("sparcial", db.String)
    partialShortName = db.Column("sparcialcorto", db.String)
    
    previousGrade = db.Column("inotaant", NUMERIC)
    currentGrade = db.Column("inotaact", NUMERIC)
    
    comment = db.Column("scomentario", db.String)
    changeDate = db.Column("dfechacambio", TIMESTAMP)
    
    studentClassroomCycleId = db.Column("idestudianteaulacic", db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "gradeId": self.gradeId,
            "cycleId": self.cycleId,
            "cycleName": self.cycleName,
            "subCycleId": self.subCycleId,
            "subCycleName": self.subCycleName,
            "courseId": self.courseId,
            "courseName": self.courseName,
            "classroomId": self.classroomId,
            "classroomName": self.classroomName,
            "courseClassroom": self.courseClassroom,
            "studentId": self.studentId,
            "studentCode": self.studentCode,
            "studentName": self.studentName,
            "subjectId": self.subjectId,
            "subjectName": self.subjectName,
            "subjectAreaId": self.subjectAreaId,
            "subjectAreaName": self.subjectAreaName,
            "partialId": self.partialId,
            "partialName": self.partialName,
            "partialShortName": self.partialShortName,
            "previousGrade": float(self.previousGrade) if self.previousGrade is not None else 0.0,
            "currentGrade": float(self.currentGrade) if self.currentGrade is not None else 0.0,
            "comment": self.comment,
            "changeDate": self.changeDate.isoformat() if self.changeDate else None,
            "studentClassroomCycleId": self.studentClassroomCycleId
        }
