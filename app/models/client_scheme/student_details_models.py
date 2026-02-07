from app import db
from sqlalchemy.dialects.postgresql import JSONB

class StudentFamily(db.Model):
    __tablename__ = "estudiantesfam"
    __table_args__ = {"schema": "cliente"}
    
    id = db.Column("idestudiantefam", db.Integer, primary_key=True)
    requestId = db.Column("idsolicitudfam", db.Integer, nullable=True)
    
    # Padre (Father)
    fatherLastName1 = db.Column("spapellido1", db.String(25), nullable=True)
    fatherLastName2 = db.Column("spapellido2", db.String(25), nullable=True)
    fatherFirstName1 = db.Column("spnombre1", db.String(50), nullable=True)
    fatherFirstName2 = db.Column("spnombre2", db.String(50), nullable=True)
    fatherDocument = db.Column("spdocumento", db.String(25), nullable=True)
    fatherDocumentTypeId = db.Column("idptipodocumento", db.Integer, nullable=True)
    fatherProfessionId = db.Column("idpprofesion", db.Integer, nullable=True)
    fatherMaritalStatusId = db.Column("idpestadocivil", db.Integer, nullable=True)
    
    # Madre (Mother)
    motherLastName1 = db.Column("smapellido1", db.String(25), nullable=True)
    motherLastName2 = db.Column("smapellido2", db.String(25), nullable=True)
    motherFirstName1 = db.Column("smnombre1", db.String(50), nullable=True)
    motherFirstName2 = db.Column("smnombre2", db.String(50), nullable=True)
    motherDocument = db.Column("smdocumento", db.String(25), nullable=True)
    motherDocumentTypeId = db.Column("idmtipodocumento", db.Integer, nullable=True)
    motherProfessionId = db.Column("idmprofesion", db.Integer, nullable=True)
    motherMaritalStatusId = db.Column("idmestadocivil", db.Integer, nullable=True)
    
    # Tutor
    tutorLastName1 = db.Column("stapellido1", db.String(25), nullable=True)
    tutorLastName2 = db.Column("stapellido2", db.String(25), nullable=True)
    tutorFirstName1 = db.Column("stnombre1", db.String(50), nullable=True)
    tutorFirstName2 = db.Column("stnombre2", db.String(50), nullable=True)
    tutorDocument = db.Column("stdocumento", db.String(25), nullable=True)
    tutorDocumentTypeId = db.Column("idttipodocumento", db.Integer, nullable=True)
    tutorProfessionId = db.Column("idtprofesion", db.Integer, nullable=True)
    tutorMaritalStatusId = db.Column("idtestadocivil", db.Integer, nullable=True)
    
    familyCode = db.Column("scodfam", db.String(10), nullable=True)
    responsibleType = db.Column("iresponsable", db.Integer, nullable=True)
    paymentFrequencyId = db.Column("idfrecuenciapago", db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "requestId": self.requestId,
            "father": {
                "lastName1": self.fatherLastName1, "lastName2": self.fatherLastName2,
                "firstName1": self.fatherFirstName1, "firstName2": self.fatherFirstName2,
                "document": self.fatherDocument, "documentTypeId": self.fatherDocumentTypeId,
                "professionId": self.fatherProfessionId, "maritalStatusId": self.fatherMaritalStatusId
            },
            "mother": {
                "lastName1": self.motherLastName1, "lastName2": self.motherLastName2,
                "firstName1": self.motherFirstName1, "firstName2": self.motherFirstName2,
                "document": self.motherDocument, "documentTypeId": self.motherDocumentTypeId,
                "professionId": self.motherProfessionId, "maritalStatusId": self.motherMaritalStatusId
            },
            "tutor": {
                "lastName1": self.tutorLastName1, "lastName2": self.tutorLastName2,
                "firstName1": self.tutorFirstName1, "firstName2": self.tutorFirstName2,
                "document": self.tutorDocument, "documentTypeId": self.tutorDocumentTypeId,
                "professionId": self.tutorProfessionId, "maritalStatusId": self.tutorMaritalStatusId
            },
            "familyCode": self.familyCode,
            "responsibleType": self.responsibleType,
            "paymentFrequencyId": self.paymentFrequencyId
        }

class StudentFamilyPhone(db.Model):
    __tablename__ = "estudiantesfamtelefono"
    __table_args__ = {"schema": "cliente"}
    id = db.Column("idestudiantefamtelefono", db.Integer, primary_key=True)
    familyId = db.Column("idestudiantefam", db.Integer, db.ForeignKey("cliente.estudiantesfam.idestudiantefam"))
    phoneTypeId = db.Column("idtipotelefono", db.Integer)
    phoneNumber = db.Column("stelefono", db.String(20))
    isPrincipal = db.Column("bprincipal", db.Boolean, default=False)
    contactTypeId = db.Column("itipocontacto", db.Integer) # 1=Padre, 2=Madre, 3=Tutor
    
    def to_dict(self):
        return {
            "id": self.id,
            "familyId": self.familyId,
            "phoneTypeId": self.phoneTypeId,
            "phoneNumber": self.phoneNumber,
            "isPrincipal": self.isPrincipal,
            "contactTypeId": self.contactTypeId
        }

class StudentFamilyEmail(db.Model):
    __tablename__ = "estudiantesfamcorreo"
    __table_args__ = {"schema": "cliente"}
    id = db.Column("idestudiantefamcorreo", db.Integer, primary_key=True)
    familyId = db.Column("idestudiantefam", db.Integer, db.ForeignKey("cliente.estudiantesfam.idestudiantefam"))
    email = db.Column("scorreo", db.String(50))
    isPrincipal = db.Column("bprincipal", db.Boolean, default=False)
    contactTypeId = db.Column("itipocontacto", db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "familyId": self.familyId,
            "email": self.email,
            "isPrincipal": self.isPrincipal,
            "contactTypeId": self.contactTypeId
        }

class StudentAllergy(db.Model):
    __tablename__ = "estudiantesalergias"
    __table_args__ = {"schema": "cliente"}
    id = db.Column("idestudiantealergia", db.Integer, primary_key=True)
    studentId = db.Column("idestudiante", db.Integer, db.ForeignKey("cliente.estudiantes.idestudiante"))
    allergyId = db.Column("idalergia", db.Integer)
    # no sobservacion in this table

class StudentMedicalPhone(db.Model):
    __tablename__ = "estudiantesmedicotelefono"
    __table_args__ = {"schema": "cliente"}
    id = db.Column("idestudiantemedicotelefono", db.Integer, primary_key=True)
    studentId = db.Column("idestudiante", db.Integer, db.ForeignKey("cliente.estudiantes.idestudiante"))
    phoneTypeId = db.Column("idtipotelefono", db.Integer)
    phoneNumber = db.Column("stelefono", db.String(20))
    isPrincipal = db.Column("bprincipal", db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "studentId": self.studentId,
            "phoneTypeId": self.phoneTypeId,
            "phoneNumber": self.phoneNumber,
            "isPrincipal": self.isPrincipal
        }
