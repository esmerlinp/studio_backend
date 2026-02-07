from app import db
from sqlalchemy.dialects.postgresql import NUMERIC

class StudentChargeBalanceView(db.Model):
    __tablename__ = 'vestudiantescargosbalance'
    __table_args__ = {'info': dict(is_view=True)}

    # Composite Primary Key candidates
    studentChargeCycleId = db.Column("idestudiantecargocic", db.Integer, primary_key=True)
    
    # Student Info
    studentId = db.Column("idestudiante", db.Integer)
    studentCode = db.Column("scodigoestudiante", db.String)
    studentName = db.Column("sestudiante", db.String)
    birthDate = db.Column("dfechanacimiento", db.Date)
    age = db.Column("iedad", db.Integer)
    genderId = db.Column("idsexo", db.Integer)
    genderName = db.Column("ssexo", db.String)
    
    # Family Info
    studentFamilyId = db.Column("idestudiantefam", db.Integer)
    familyCode = db.Column("scodfam", db.String)
    
    # Academic Info
    cycleId = db.Column("idciclo", db.Integer)
    cycleName = db.Column("sciclo", db.String)
    levelId = db.Column("idnivel", db.Integer)
    levelName = db.Column("snivel", db.String)
    courseId = db.Column("idcurso", db.Integer)
    classroomId = db.Column("idaula", db.Integer)
    courseClassroomName = db.Column("scursoaula", db.String)
    studentCycleClassroomId = db.Column("idestudianteaulacic", db.Integer)

    # Charge Info
    conceptId = db.Column("idconcepto", db.Integer)
    conceptName = db.Column("sconcepto", db.String)
    isFamily = db.Column("bfamiliar", db.Boolean)
    isRecurrent = db.Column("brecurrente", db.Boolean)
    quota = db.Column("icuota", db.Integer)
    
    # Financials
    chargeAmount = db.Column("nmontocargo", NUMERIC)
    totalSurcharges = db.Column("ntotal_recargos", NUMERIC)
    totalDiscounts = db.Column("ntotal_descuentos", NUMERIC)
    totalItbis = db.Column("ntotal_itbis", NUMERIC)
    totalPaid = db.Column("ntotal_pagado", NUMERIC)
    balance = db.Column("nbalance", NUMERIC)
    
    # Responsible Info
    responsibleId = db.Column("iresponsable", db.Integer)
    responsibleType = db.Column("stiporesponsable", db.String)
    responsibleName = db.Column("snombreresponsable", db.String)
    responsiblePhone = db.Column("stelefonoresponsable", db.String)
    responsibleEmail = db.Column("scorreoresponsable", db.String)

    def to_dict(self):
        return {
            "studentChargeCycleId": self.studentChargeCycleId,
            "studentId": self.studentId,
            "studentCode": self.studentCode,
            "studentName": self.studentName,
            "birthDate": self.birthDate.isoformat() if self.birthDate else None,
            "age": self.age,
            "genderId": self.genderId,
            "genderName": self.genderName,
            "studentFamilyId": self.studentFamilyId,
            "familyCode": self.familyCode,
            "cycleId": self.cycleId,
            "cycleName": self.cycleName,
            "levelId": self.levelId,
            "levelName": self.levelName,
            "courseId": self.courseId,
            "classroomId": self.classroomId,
            "courseClassroomName": self.courseClassroomName,
            "studentCycleClassroomId": self.studentCycleClassroomId,
            "conceptId": self.conceptId,
            "conceptName": self.conceptName,
            "isFamily": self.isFamily,
            "isRecurrent": self.isRecurrent,
            "quota": self.quota,
            "chargeAmount": float(self.chargeAmount) if self.chargeAmount is not None else 0.0,
            "totalSurcharges": float(self.totalSurcharges) if self.totalSurcharges is not None else 0.0,
            "totalDiscounts": float(self.totalDiscounts) if self.totalDiscounts is not None else 0.0,
            "totalItbis": float(self.totalItbis) if self.totalItbis is not None else 0.0,
            "totalPaid": float(self.totalPaid) if self.totalPaid is not None else 0.0,
            "balance": float(self.balance) if self.balance is not None else 0.0,
            "responsibleId": self.responsibleId,
            "responsibleType": self.responsibleType,
            "responsibleName": self.responsibleName,
            "responsiblePhone": self.responsiblePhone,
            "responsibleEmail": self.responsibleEmail
        }
