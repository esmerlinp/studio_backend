from app import db

class ActiveCycleStudentView(db.Model):
    __tablename__ = 'vestudiantescicloactivo'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    studentCycleClassroomId = db.Column("idestudianteaulacic", db.Integer, primary_key=True)

    # Columns
    studentId = db.Column("idestudiante", db.Integer)
    cycleId = db.Column("idciclo", db.Integer)
    classroomId = db.Column("idaula", db.Integer)
    courseId = db.Column("idcurso", db.Integer)
    
    studentCode = db.Column("scodigoestudiante", db.String)
    studentName = db.Column("sestudiante", db.String)
    courseClassroomName = db.Column("scursoaula", db.String)
    
    genderId = db.Column("idsexo", db.Integer)
    cycleName = db.Column("sciclo", db.String)
    courseName = db.Column("scurso", db.String)
    classroomName = db.Column("saula", db.String)
    
    studentStatus = db.Column("iestadoestudiante", db.Integer)
    levelId = db.Column("idnivel", db.Integer)

    def to_dict(self):
        return {
            "studentCycleClassroomId": self.studentCycleClassroomId,
            "studentId": self.studentId,
            "cycleId": self.cycleId,
            "classroomId": self.classroomId,
            "courseId": self.courseId,
            "studentCode": self.studentCode,
            "studentName": self.studentName,
            "courseClassroomName": self.courseClassroomName,
            "genderId": self.genderId,
            "cycleName": self.cycleName,
            "courseName": self.courseName,
            "classroomName": self.classroomName,
            "studentStatus": self.studentStatus,
            "levelId": self.levelId
        }
