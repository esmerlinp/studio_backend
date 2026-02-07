from app import db

class RequestListView(db.Model):
    __tablename__ = 'vlistasolicitudes'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idsolicitud", db.Integer, primary_key=True)

    # Columns
    applicantName = db.Column("ssolicitante", db.String)
    
    courseId = db.Column("idcurso", db.Integer)
    courseName = db.Column("scurso", db.String)
    
    responsibleName = db.Column("snombreresponsable", db.String)
    responsiblePhone = db.Column("stelefonoresponsable", db.String)
    
    evaluationState = db.Column("iestadoevaluacion", db.Integer)
    isInscribed = db.Column("binscrito", db.Boolean)
    requestProcessState = db.Column("sestadoprocesosolicitud", db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "applicantName": self.applicantName,
            "courseId": self.courseId,
            "courseName": self.courseName,
            "responsibleName": self.responsibleName,
            "responsiblePhone": self.responsiblePhone,
            "evaluationState": self.evaluationState,
            "isInscribed": self.isInscribed,
            "requestProcessState": self.requestProcessState
        }
