from app import db
from datetime import datetime

class AdmissionRequest(db.Model):
    __tablename__ = 'solicitudes'
    
    id = db.Column("idsolicitud", db.Integer, primary_key=True)
    applicantName = db.Column("ssolicitante", db.String(200), nullable=False)
    cycleId = db.Column("idciclo", db.Integer, nullable=False)
    requestDate = db.Column("dfechasolicitud", db.DateTime, default=datetime.utcnow)
    courseId = db.Column("idcurso", db.Integer, nullable=False)
    
    # States: 1=Pending, 2=Evaluated, etc. (Inferred)
    evaluationState = db.Column("iestadoevaluacion", db.Integer, default=1)
    isInscribed = db.Column("binscrito", db.Boolean, default=False)
    requestProcessState = db.Column("sestadoprocesosolicitud", db.String(50), default='PENDIENTE')
    
    responsibleName = db.Column("snombreresponsable", db.String(200), nullable=True)
    responsiblePhone = db.Column("stelefonoresponsable", db.String(20), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "applicantName": self.applicantName,
            "cycleId": self.cycleId,
            "requestDate": self.requestDate.isoformat() if self.requestDate else None,
            "courseId": self.courseId,
            "evaluationState": self.evaluationState,
            "isInscribed": self.isInscribed,
            "requestProcessState": self.requestProcessState,
            "responsibleName": self.responsibleName,
            "responsiblePhone": self.responsiblePhone
        }
