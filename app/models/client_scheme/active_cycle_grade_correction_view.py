from app import db
from sqlalchemy.dialects.postgresql import NUMERIC, TIMESTAMP

class ActiveCycleGradeCorrectionView(db.Model):
    __tablename__ = 'vnotascorrecionescicloactivo'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idnotacorreccion", db.Integer, primary_key=True)

    # Columns
    requestDate = db.Column("dfechasolicitud", TIMESTAMP)
    processedDate = db.Column("dfechaprocesada", TIMESTAMP)
    
    studentId = db.Column("idestudiante", db.Integer)
    studentName = db.Column("snombreresponsable", db.String)
    
    levelId = db.Column("idnivel", db.Integer)
    levelName = db.Column("snivel", db.String)
    
    courseId = db.Column("idcurso", db.Integer)
    courseName = db.Column("scurso", db.String)
    
    cycleId = db.Column("idciclo", db.Integer)
    cycleName = db.Column("sciclo", db.String)
    
    subjectId = db.Column("idasignatura", db.Integer)
    subjectName = db.Column("sasignatura", db.String)
    
    teacherId = db.Column("idprofesor", db.Integer)
    teacherName = db.Column("sprofesor", db.String)
    
    partialId = db.Column("idparcial", db.Integer)
    partialName = db.Column("sparcial", db.String)
    
    competencyId = db.Column("idcompetencia", db.Integer)
    competencyName = db.Column("scompetencia", db.String)
    
    oldGrade = db.Column("nnotaant", NUMERIC)
    newGrade = db.Column("nnotanueva", NUMERIC)
    
    status = db.Column("sestado", db.String)
    reason = db.Column("smotivo", db.String)
    observation = db.Column("scomentario", db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "requestDate": self.requestDate.isoformat() if self.requestDate else None,
            "processedDate": self.processedDate.isoformat() if self.processedDate else None,
            "studentId": self.studentId,
            "studentName": self.studentName,
            "levelId": self.levelId,
            "levelName": self.levelName,
            "courseId": self.courseId,
            "courseName": self.courseName,
            "cycleId": self.cycleId,
            "cycleName": self.cycleName,
            "subjectId": self.subjectId,
            "subjectName": self.subjectName,
            "teacherId": self.teacherId,
            "teacherName": self.teacherName,
            "partialId": self.partialId,
            "partialName": self.partialName,
            "competencyId": self.competencyId,
            "competencyName": self.competencyName,
            "oldGrade": float(self.oldGrade) if self.oldGrade is not None else 0.0,
            "newGrade": float(self.newGrade) if self.newGrade is not None else 0.0,
            "status": self.status,
            "reason": self.reason,
            "observation": self.observation
        }
