from app import db

class ActiveCycleAttendanceView(db.Model):
    __tablename__ = 'vasistenciascicloactivo'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key (Attendance ID should be unique)
    attendanceId = db.Column("idasistencia", db.Integer, primary_key=True)

    # Columns
    date = db.Column("dfecha", db.Date)
    comment = db.Column("scomentario", db.String)
    attendanceTypeId = db.Column("idtipoasistencia", db.Integer)
    attendanceTypeName = db.Column("stipoasistencia", db.String)
    
    studentId = db.Column("idestudiante", db.Integer)
    studentCode = db.Column("scodigoestudiante", db.String)
    studentName = db.Column("sestudiante", db.String)
    birthDate = db.Column("dfechanacimiento", db.Date)
    age = db.Column("iedad", db.Integer)
    genderId = db.Column("idsexo", db.Integer)
    genderName = db.Column("ssexo", db.String)
    
    cycleId = db.Column("idciclo", db.Integer)
    cycleName = db.Column("sciclo", db.String)
    
    levelId = db.Column("idnivel", db.Integer)
    levelName = db.Column("snivel", db.String)
    
    courseId = db.Column("idcurso", db.Integer)
    classroomId = db.Column("idaula", db.Integer)
    courseClassroomName = db.Column("scursoaula", db.String)
    
    studentCycleClassroomId = db.Column("idestudianteaulacic", db.Integer)

    def to_dict(self):
        return {
            "attendanceId": self.attendanceId,
            "date": self.date.isoformat() if self.date else None,
            "comment": self.comment,
            "attendanceTypeId": self.attendanceTypeId,
            "attendanceTypeName": self.attendanceTypeName,
            "studentId": self.studentId,
            "studentCode": self.studentCode,
            "studentName": self.studentName,
            "birthDate": self.birthDate.isoformat() if self.birthDate else None,
            "age": self.age,
            "genderId": self.genderId,
            "genderName": self.genderName,
            "cycleId": self.cycleId,
            "cycleName": self.cycleName,
            "levelId": self.levelId,
            "levelName": self.levelName,
            "courseId": self.courseId,
            "classroomId": self.classroomId,
            "courseClassroomName": self.courseClassroomName,
            "studentCycleClassroomId": self.studentCycleClassroomId
        }
