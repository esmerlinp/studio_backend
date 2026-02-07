from app import db
from sqlalchemy.dialects.postgresql import TIMESTAMP

class StudentListView(db.Model):
    __tablename__ = 'vlistaestudiantes'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idestudiante", db.Integer, primary_key=True)

    # Columns
    studentCode = db.Column("scodigoestudiante", db.String)
    fullName = db.Column("sestudiante", db.String)
    birthDate = db.Column("dfechanacimiento", TIMESTAMP)
    age = db.Column("iedad", db.Integer)
    inscriptionDate = db.Column("dfechainscripcion", TIMESTAMP)
    
    levelId = db.Column("idnivel", db.Integer)
    levelName = db.Column("snivel", db.String)
    
    courseId = db.Column("idcurso", db.Integer)
    classroomId = db.Column("idaula", db.Integer)
    courseClassroom = db.Column("scursoaula", db.String)
    
    cycleId = db.Column("idciclo", db.Integer)
    cycleName = db.Column("sciclo", db.String)
    
    responsibleType = db.Column("iresponsable", db.Integer)
    responsibleName = db.Column("snombreresponsable", db.String)
    responsiblePhone = db.Column("stelefonoresponsable", db.String)
    responsibleEmail = db.Column("scorreoresponsable", db.String)
    
    familyCode = db.Column("scodfam", db.String)
    
    studentStateId = db.Column("iestadoestudiante", db.Integer)
    studentState = db.Column("sestadoestudiante", db.String)
    
    sexId = db.Column("idsexo", db.Integer)
    sex = db.Column("ssexo", db.String)
    
    livesWithId = db.Column("ivive", db.Integer)
    livesWith = db.Column("svive", db.String)
    
    countryId = db.Column("idpais", db.Integer)
    country = db.Column("spais", db.String)
    
    cityId = db.Column("idciudad", db.Integer)
    city = db.Column("sciudad", db.String)
    
    sectorId = db.Column("idsector", db.Integer)
    sector = db.Column("ssector", db.String)
    
    address = db.Column("sdireccion", db.String)
    
    previousSchoolId = db.Column("idcolegioprocedencia", db.Integer)
    previousSchool = db.Column("scolegioprocedencia", db.String)
    
    bloodTypeId = db.Column("idtiposangre", db.Integer)
    bloodType = db.Column("stiposangre", db.String)
    
    doctorName = db.Column("snombremedico", db.String)
    doctorPhone = db.Column("stelefonomedico", db.String)
    medicalInsuranceNumber = db.Column("snumeroseguromedico", db.String)
    
    medicalInstitutionId = db.Column("idinstitucionmedica", db.Integer)
    medicalInstitution = db.Column("sinstitucionmedica", db.String)
    
    insuranceCompanyId = db.Column("idinstitucionsegmed", db.Integer)
    insuranceCompany = db.Column("sinstitucionsegmed", db.String)
    
    requestId = db.Column("idsolicitud", db.Integer)
    studentFamilyId = db.Column("idestudiantefam", db.Integer)
    studentClassroomCycleId = db.Column("idestudianteaulacic", db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "studentCode": self.studentCode,
            "fullName": self.fullName,
            "birthDate": self.birthDate.isoformat() if self.birthDate else None,
            "age": self.age,
            "inscriptionDate": self.inscriptionDate.isoformat() if self.inscriptionDate else None,
            "levelId": self.levelId,
            "levelName": self.levelName,
            "courseId": self.courseId,
            "classroomId": self.classroomId,
            "courseClassroom": self.courseClassroom,
            "cycleId": self.cycleId,
            "cycleName": self.cycleName,
            "responsibleType": self.responsibleType,
            "responsibleName": self.responsibleName,
            "responsiblePhone": self.responsiblePhone,
            "responsibleEmail": self.responsibleEmail,
            "familyCode": self.familyCode,
            "studentStateId": self.studentStateId,
            "studentState": self.studentState,
            "sexId": self.sexId,
            "sex": self.sex,
            "livesWithId": self.livesWithId,
            "livesWith": self.livesWith,
            "countryId": self.countryId,
            "country": self.country,
            "cityId": self.cityId,
            "city": self.city,
            "sectorId": self.sectorId,
            "sector": self.sector,
            "address": self.address,
            "previousSchoolId": self.previousSchoolId,
            "previousSchool": self.previousSchool,
            "bloodTypeId": self.bloodTypeId,
            "bloodType": self.bloodType,
            "doctorName": self.doctorName,
            "doctorPhone": self.doctorPhone,
            "medicalInsuranceNumber": self.medicalInsuranceNumber,
            "medicalInstitutionId": self.medicalInstitutionId,
            "medicalInstitution": self.medicalInstitution,
            "insuranceCompanyId": self.insuranceCompanyId,
            "insuranceCompany": self.insuranceCompany,
            "requestId": self.requestId,
            "studentFamilyId": self.studentFamilyId,
            "studentClassroomCycleId": self.studentClassroomCycleId
        }
