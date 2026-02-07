from app import db
from sqlalchemy.dialects.postgresql import TIMESTAMP

class InscriptionListView(db.Model):
    __tablename__ = 'vlistainscripcionest'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idsolicitud", db.Integer, primary_key=True)

    # Columns
    cycleId = db.Column("idciclo", db.Integer)
    cycleName = db.Column("sciclo", db.String)
    
    studentName = db.Column("sestudiante", db.String)
    birthDate = db.Column("dfechanacimiento", TIMESTAMP)
    
    sex = db.Column("ssexo", db.String)
    
    courseId = db.Column("idcurso", db.Integer)
    courseName = db.Column("scurso", db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "cycleId": self.cycleId,
            "cycleName": self.cycleName,
            "studentName": self.studentName,
            "birthDate": self.birthDate.isoformat() if self.birthDate else None,
            "sex": self.sex,
            "courseId": self.courseId,
            "courseName": self.courseName
        }
