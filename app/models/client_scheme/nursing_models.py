from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class NursingVisit(db.Model):
    __tablename__ = "enfermeria_visitas"
    __table_args__ = {"schema": "cliente"}


    id = db.Column("idvisita", db.Integer, primary_key=True)
    studentId = db.Column("idestudiante", db.Integer, db.ForeignKey("cliente.estudiantes.idestudiante"), nullable=False)
    date = db.Column("dfecha", db.DateTime, default=datetime.utcnow, nullable=False)
    
    reason = db.Column("smotivo", db.String(200), nullable=True)  # Headache, Fever, etc.
    symptoms = db.Column("ssintomas", db.Text, nullable=True)
    treatment = db.Column("stratamiento", db.Text, nullable=True) # Meds given, ice pack, etc.
    outcome = db.Column("sresultado", db.String(100), nullable=True) # Returned to class, Sent home, Hospital
    
    parentNotified = db.Column("bpadrenotificado", db.Boolean, default=False)
    nurseNotes = db.Column("snotas", db.Text, nullable=True)
    
    # Vital signs stored as JSON: {"temp": 37.5, "bp": "120/80", "hr": 80}
    vitalSigns = db.Column("jsignosvitales", JSONB, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "studentId": self.studentId,
            "date": self.date.isoformat(),
            "reason": self.reason,
            "symptoms": self.symptoms,
            "treatment": self.treatment,
            "outcome": self.outcome,
            "parentNotified": self.parentNotified,
            "nurseNotes": self.nurseNotes,
            "vitalSigns": self.vitalSigns
        }

class NursingInventory(db.Model):
    __tablename__ = "enfermeria_inventario"
    __table_args__ = {"schema": "cliente"}


    id = db.Column("idinventario", db.Integer, primary_key=True)
    itemName = db.Column("snombreitem", db.String(100), nullable=False)
    description = db.Column("sdescripcion", db.String(255), nullable=True)
    quantity = db.Column("icantidad", db.Integer, default=0)
    unit = db.Column("sunidad", db.String(50), nullable=True) # tablets, ml, box
    expirationDate = db.Column("dfechacaducidad", db.Date, nullable=True)
    minThreshold = db.Column("iminimo", db.Integer, default=5) # Alert threshold

    def to_dict(self):
        return {
            "id": self.id,
            "itemName": self.itemName,
            "description": self.description,
            "quantity": self.quantity,
            "unit": self.unit,
            "expirationDate": self.expirationDate.isoformat() if self.expirationDate else None,
            "minThreshold": self.minThreshold
        }

class StudentCondition(db.Model):
    __tablename__ = "estudiantes_condiciones"
    __table_args__ = {"schema": "cliente"}


    id = db.Column("idcondicion", db.Integer, primary_key=True)
    studentId = db.Column("idestudiante", db.Integer, db.ForeignKey("cliente.estudiantes.idestudiante"), nullable=False)
    conditionName = db.Column("snombrecondicion", db.String(100), nullable=False)
    description = db.Column("sdescripcion", db.Text, nullable=True)
    careInstructions = db.Column("sinstrucciones", db.Text, nullable=True)
    isCritical = db.Column("bcritica", db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "studentId": self.studentId,
            "conditionName": self.conditionName,
            "description": self.description,
            "careInstructions": self.careInstructions,
            "isCritical": self.isCritical
        }

class StudentVaccine(db.Model):
    __tablename__ = "estudiantes_vacunas"
    __table_args__ = {"schema": "cliente"}


    id = db.Column("idvacuna", db.Integer, primary_key=True)
    studentId = db.Column("idestudiante", db.Integer, db.ForeignKey("cliente.estudiantes.idestudiante"), nullable=False)
    vaccineName = db.Column("snombrevacuna", db.String(100), nullable=False)
    dateAdministered = db.Column("dfechaaplicacion", db.Date, nullable=True)
    doseNumber = db.Column("indosis", db.Integer, nullable=True) # 1st, 2nd, Booster

    def to_dict(self):
        return {
            "id": self.id,
            "studentId": self.studentId,
            "vaccineName": self.vaccineName,
            "dateAdministered": self.dateAdministered.isoformat() if self.dateAdministered else None,
            "doseNumber": self.doseNumber
        }

class MedicationAuthorization(db.Model):
    __tablename__ = "estudiantes_autorizaciones_med"
    __table_args__ = {"schema": "cliente"}

    id = db.Column("idautorizacion", db.Integer, primary_key=True)
    studentId = db.Column("idestudiante", db.Integer, db.ForeignKey("cliente.estudiantes.idestudiante"), nullable=False)
    medicationName = db.Column("snombremedicamento", db.String(100), nullable=False)
    dosage = db.Column("sdosis", db.String(50), nullable=True)
    frequency = db.Column("sfrecuencia", db.String(100), nullable=True)
    
    startDate = db.Column("dfechainicio", db.Date, nullable=False)
    endDate = db.Column("dfechafin", db.Date, nullable=True)
    
    authorizedBy = db.Column("sautorizadopor", db.String(100), nullable=False) # Name of parent/guardian
    authorizationDate = db.Column("dfechaautorizacion", db.DateTime, default=datetime.utcnow)
    signatureUrl = db.Column("srutafirma", db.String(255), nullable=True) # Binary or path to signature img
    
    isActive = db.Column("bactivo", db.Boolean, default=True)
    notes = db.Column("snotas", db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "studentId": self.studentId,
            "medicationName": self.medicationName,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "startDate": self.startDate.isoformat() if self.startDate else None,
            "endDate": self.endDate.isoformat() if self.endDate else None,
            "authorizedBy": self.authorizedBy,
            "authorizationDate": self.authorizationDate.isoformat(),
            "isActive": self.isActive,
            "notes": self.notes
        }

class StudentEmergencyContact(db.Model):
    __tablename__ = "estudiantes_contactos_emergencia"
    __table_args__ = {"schema": "cliente"}

    id = db.Column("idcontacto", db.Integer, primary_key=True)
    studentId = db.Column("idestudiante", db.Integer, db.ForeignKey("cliente.estudiantes.idestudiante"), nullable=False)
    name = db.Column("snombre", db.String(100), nullable=False)
    relationship = db.Column("sparentesco", db.String(50), nullable=False) # Uncle, Neighbor, etc.
    phone1 = db.Column("stelefono1", db.String(20), nullable=False)
    phone2 = db.Column("stelefono2", db.String(20), nullable=True)
    priority = db.Column("iprioridad", db.Integer, default=1) # 1 = First call

    def to_dict(self):
        return {
            "id": self.id,
            "studentId": self.studentId,
            "name": self.name,
            "relationship": self.relationship,
            "phone1": self.phone1,
            "phone2": self.phone2,
            "priority": self.priority
        }
