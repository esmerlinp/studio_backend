from app import db
from sqlalchemy.dialects.postgresql import TIMESTAMP

class EvaluationRequestListView(db.Model):
    __tablename__ = 'vlistaevalsolicitudes'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idsolicitud", db.Integer, primary_key=True)

    # Columns
    courseId = db.Column("idcurso", db.Integer)
    courseName = db.Column("scurso", db.String)
    
    sexId = db.Column("idsexo", db.Integer)
    sex = db.Column("ssexo", db.String)
    
    evaluatorId = db.Column("idempevaluador", db.Integer)
    studentName = db.Column("sestudiante", db.String)
    
    birthDate = db.Column("dfechanacimiento", TIMESTAMP)
    decision = db.Column("sdecision", db.String)
    
    evaluatorName = db.Column("sevaluador", db.String)
    evaluationDate = db.Column("dfechaevaluacion", TIMESTAMP)
    
    evaluationState = db.Column("iestadoevaluacion", db.Integer)
    isInscribed = db.Column("binscrito", db.Boolean)
    
    cycleId = db.Column("idciclo", db.Integer)
    cycleName = db.Column("sciclo", db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "courseId": self.courseId,
            "courseName": self.courseName,
            "sexId": self.sexId,
            "sex": self.sex,
            "evaluatorId": self.evaluatorId,
            "studentName": self.studentName,
            "birthDate": self.birthDate.isoformat() if self.birthDate else None,
            "decision": self.decision,
            "evaluatorName": self.evaluatorName,
            "evaluationDate": self.evaluationDate.isoformat() if self.evaluationDate else None,
            "evaluationState": self.evaluationState,
            "isInscribed": self.isInscribed,
            "cycleId": self.cycleId,
            "cycleName": self.cycleName
        }
