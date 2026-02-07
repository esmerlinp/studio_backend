from app import db
from sqlalchemy.dialects.postgresql import NUMERIC

class ActiveCycleStudentGradeView(db.Model):
    __tablename__ = 'vnotasestudiantescicloactivo'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idregistro", db.Integer, primary_key=True)

    # Columns
    studentId = db.Column("idestudiante", db.Integer)
    studentName = db.Column("snombreresponsable", db.String)
    
    courseId = db.Column("idcurso", db.Integer)
    courseName = db.Column("scurso", db.String)
    
    cycleId = db.Column("idciclo", db.Integer)
    
    subjectId = db.Column("idasignatura", db.Integer)
    subjectName = db.Column("sasignatura", db.String)
    
    partialId = db.Column("idparcial", db.Integer)
    partialName = db.Column("sparcial", db.String)
    
    competencyId = db.Column("idcompetencia", db.Integer)
    competencyName = db.Column("scompetencia", db.String)
    
    grade = db.Column("nnota", NUMERIC)
    literal = db.Column("sliteral", db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "studentId": self.studentId,
            "studentName": self.studentName,
            "courseId": self.courseId,
            "courseName": self.courseName,
            "cycleId": self.cycleId,
            "subjectId": self.subjectId,
            "subjectName": self.subjectName,
            "partialId": self.partialId,
            "partialName": self.partialName,
            "competencyId": self.competencyId,
            "competencyName": self.competencyName,
            "grade": float(self.grade) if self.grade is not None else 0.0,
            "literal": self.literal
        }
