from app import db

class ActiveCycleCourseView(db.Model):
    __tablename__ = 'vasignaturascursocicloactivo'
    __table_args__ = {'info': dict(is_view=True)}

    # Composite Primary Key for SQLAlchemy mapping purposes (since views don't have PKs)
    # Using the combination of IDs that define uniqueness
    cycleId = db.Column("idciclo", db.Integer, primary_key=True)
    subCycleId = db.Column("idsubciclo", db.Integer, primary_key=True)
    courseId = db.Column("idcurso", db.Integer, primary_key=True)
    subjectId = db.Column("idasignatura", db.Integer, primary_key=True)

    # Columns
    cycleName = db.Column("sciclo", db.String)
    subCycleName = db.Column("ssubciclo", db.String)
    subCycleOrder = db.Column("iordensubcic", db.Integer)
    courseName = db.Column("scurso", db.String)
    courseOrder = db.Column("iordencurso", db.Integer, nullable=True) # Assuming it might be nullable based on SQL
    subjectName = db.Column("sasignatura", db.String)
    areaId = db.Column("idareatematica", db.Integer)
    areaName = db.Column("sareatematica", db.String)
    subjectOrder = db.Column("iordenasignatura", db.Integer)
    subjectCredits = db.Column("icreditosasignatura", db.Integer)

    def to_dict(self):
        return {
            "cycleId": self.cycleId,
            "cycleName": self.cycleName,
            "subCycleId": self.subCycleId,
            "subCycleName": self.subCycleName,
            "subCycleOrder": self.subCycleOrder,
            "courseId": self.courseId,
            "courseName": self.courseName,
            "courseOrder": self.courseOrder,
            "subjectId": self.subjectId,
            "subjectName": self.subjectName,
            "subjectOrder": self.subjectOrder,
            "subjectCredits": self.subjectCredits,
            "areaId": self.areaId,
            "areaName": self.areaName
        }
