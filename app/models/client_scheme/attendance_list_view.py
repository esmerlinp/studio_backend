from app import db

class AttendanceListView(db.Model):
    __tablename__ = 'vlistaasistencias'
    __table_args__ = {'schema': 'cliente', 'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idasistencia", db.Integer, primary_key=True)

    # Columns
    date = db.Column("dfecha", db.Date)
    comment = db.Column("scomentario", db.String)
    
    attendanceTypeId = db.Column("idtipoasistencia", db.Integer)
    attendanceTypeName = db.Column("stipoasistencia", db.String)
    
    studentId = db.Column("idestudiante", db.Integer)
    studentCode = db.Column("scodigoestudiante", db.String)
    studentName = db.Column("sestudiante", db.String)
    studentCycleClassroomId = db.Column("idestudianteaulacic", db.Integer)
    
    # ... other student info columns if needed, keeping it minimal for now as per view def
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

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "comment": self.comment,
            "attendanceTypeId": self.attendanceTypeId,
            "attendanceTypeName": self.attendanceTypeName,
            "studentId": self.studentId,
            "studentCode": self.studentCode,
            "studentName": self.studentName,
            "studentCycleClassroomId": self.studentCycleClassroomId,
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
            "courseClassroomName": self.courseClassroomName
        }
