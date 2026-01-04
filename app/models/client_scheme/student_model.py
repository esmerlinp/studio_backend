from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from app import db 

class Student(db.Model):
    __tablename__ = "estudiantes"

    # --- CAMPOS FIJOS (CamelCase) ---
    id = db.Column("idestudiante", db.Integer, primary_key=True)
    requestId = db.Column("idsolicitud", db.Integer, nullable=True)
    #requestId = db.Column("idsolicitud", db.Integer, db.ForeignKey("cliente.solicitudes.idsolicitud"), nullable=True)
    studentCode = db.Column("scodigoestudiante", db.String(25), nullable=False)
    enrollmentDate = db.Column("dfechainscripcion", db.Date, nullable=False, default=datetime.utcnow)
    
    firstName = db.Column("sestnombre1", db.String(50), nullable=False)
    middleName = db.Column("sestnombre2", db.String(50), nullable=True) 
    lastName = db.Column("sestapellido1", db.String(25), nullable=False) # Primer apellido
    secondLastName = db.Column("sestapellido2", db.String(25), nullable=True) # Segundo apellido
    
    genderId = db.Column("idsexo", db.Integer, nullable=False)
    livingSituation = db.Column("ivive", db.SmallInteger, nullable=False)
    birthDate = db.Column("dfechanacimiento", db.Date, nullable=False)
    
    countryId = db.Column("idpais", db.Integer, nullable=True)
    cityId = db.Column("idciudad", db.Integer, nullable=True)
    sectorId = db.Column("idsector", db.Integer, nullable=True)
    address = db.Column("sdireccion", db.String(300), nullable=True)
    
    previousSchoolId = db.Column("idcolegioprocedencia", db.Integer, nullable=True)
    entryReason = db.Column("smotivoentrada", db.Text, nullable=True)
    exitReason = db.Column("smotivosalida", db.Text, nullable=True)
    status = db.Column("iestadoestudiante", db.SmallInteger, nullable=False, default=1)
    
    familyId = db.Column("idestudiantefam", db.Integer, nullable=True)
    #familyId = db.Column("idestudiantefam", db.Integer, db.ForeignKey("cliente.estudiantesfam.idestudiantefam"), nullable=True)
    bloodTypeId = db.Column("idtiposangre", db.SmallInteger, nullable=True)
    doctorName = db.Column("snombremedico", db.String(50), nullable=True)
    insuranceNumber = db.Column("snumeroseguromedico", db.String(25), nullable=True)
    
    photoUrl = db.Column("srutafoto", db.String(250), nullable=True)
    photoCardUrl = db.Column("srutaimgsegmed", db.String(250), nullable=True)
    
    medicalInstitutionId = db.Column("idinstitucionmedica", db.SmallInteger, nullable=True)
    insuranceInstitutionId = db.Column("idinstitucionsegmed", db.SmallInteger, nullable=True)
    
    custom_attributes = db.Column("jatributos", JSONB, nullable=False, server_default='{}')

    def __repr__(self):
        return f"<Student {self.firstName} {self.lastName} (Code: {self.studentCode})>"

    def to_dict(self, include_sensitive=False):
        # Nombre completo considerando los 4 posibles campos
        name_parts = [self.firstName, self.middleName, self.lastName, self.secondLastName]
        full_name = " ".join(filter(None, name_parts))

        data = {
            "id": self.id,
            "requestId": self.requestId,
            "studentCode": self.studentCode,
            "firstName": self.firstName,
            "middleName": self.middleName,
            "lastName": self.lastName,
            "secondLastName": self.secondLastName,
            "fullName": full_name,
            "genderId": self.genderId,
            "enrollmentDate": self.enrollmentDate.isoformat() if self.enrollmentDate else None,
            "status": self.status,
            "previousSchoolId": self.previousSchoolId,
            "custom_attributes": self.custom_attributes
        }

        if include_sensitive:
            data.update({
                "birthDate": self.birthDate.isoformat() if self.birthDate else None,
                "livingSituation": self.livingSituation,
                "address": self.address,
                "countryId": self.countryId,
                "cityId": self.cityId,
                "sectorId": self.sectorId,
                "familyId": self.familyId,
                "bloodTypeId": self.bloodTypeId,
                "doctorName": self.doctorName,
                "insuranceNumber": self.insuranceNumber,
                "insuranceInstitutionId": self.insuranceInstitutionId,
                "medicalInstitutionId": self.medicalInstitutionId,
                "photoCardUrl": self.photoCardUrl,
                "entryReason": self.entryReason,
                "exitReason": self.exitReason
            })
            
        return data