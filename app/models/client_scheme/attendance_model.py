from app import db
from datetime import datetime

class Attendance(db.Model):
    __tablename__ = 'asistencias'
    __table_args__ = {'schema': 'cliente'}

    attendanceId = db.Column("idasistencia", db.Integer, primary_key=True, autoincrement=True)
    studentCycleClassroomId = db.Column("idestudianteaulacic", db.Integer, db.ForeignKey('cliente.estudiantesaulacic.idestudianteaulacic'), nullable=False)
    date = db.Column("dfecha", db.Date, nullable=False, default=datetime.utcnow)
    attendanceTypeId = db.Column("idtipoasistencia", db.SmallInteger, nullable=False)
    comment = db.Column("scomentario", db.Text)

    def to_dict(self):
        return {
            "attendanceId": self.attendanceId,
            "studentCycleClassroomId": self.studentCycleClassroomId,
            "date": self.date.isoformat() if self.date else None,
            "attendanceTypeId": self.attendanceTypeId,
            "comment": self.comment
        }
