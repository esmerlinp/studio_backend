from app import db
from datetime import datetime
from app.models.client_scheme.nursing_models import (
    NursingVisit, MedicationAuthorization, StudentEmergencyContact, StudentCondition
)
from app.services.event_bus_service import emit_event, Events

def create_nursing_visit(data):
    """
    Record a new nursing visit.
    Validates medication authorization if treatment involves meds.
    """
    student_id = data.get('studentId')
    reason = data.get('reason')
    treatment = data.get('treatment')
    
    # Logic: If treatment contains a known medication, check for authorization
    # For now, we'll look for a flag 'isMedication' in the payload or simple string matching
    if data.get('isMedication'):
        med_name = data.get('medicationName')
        if not med_name:
            return None, "Se requiere el nombre del medicamento para validación"
            
        # Check for active authorization
        auth = MedicationAuthorization.query.filter_by(
            studentId=student_id, 
            medicationName=med_name,
            isActive=True
        ).first()
        
        if not auth or (auth.endDate and auth.endDate < datetime.utcnow().date()):
            return None, f"No hay autorización válida para suministrar {med_name}"

    visit = NursingVisit(
        studentId=student_id,
        reason=reason,
        symptoms=data.get('symptoms'),
        treatment=treatment,
        outcome=data.get('outcome'),
        vitalSigns=data.get('vitalSigns'),
        nurseNotes=data.get('nurseNotes')
    )
    
    db.session.add(visit)
    db.session.commit()
    
    # Emit event for parent notification and academic tracking
    emit_event(Events.STUDENT_HEALTH_VISIT, {
        "visitId": visit.id,
        "studentId": student_id,
        "reason": reason,
        "outcome": visit.outcome
    })
    
    return visit.id, None

def get_student_health_profile(student_id):
    """
    Consolidate health data for the Student 360 view.
    """
    conditions = StudentCondition.query.filter_by(studentId=student_id).all()
    authorizations = MedicationAuthorization.query.filter_by(studentId=student_id, isActive=True).all()
    contacts = StudentEmergencyContact.query.filter_by(studentId=student_id).order_by(StudentEmergencyContact.priority).all()
    visits = NursingVisit.query.filter_by(studentId=student_id).order_by(NursingVisit.date.desc()).limit(10).all()
    
    return {
        "conditions": [c.to_dict() for c in conditions],
        "activeAuthorizations": [a.to_dict() for a in authorizations],
        "emergencyContacts": [contact.to_dict() for contact in contacts],
        "recentVisits": [v.to_dict() for v in visits]
    }

def add_medication_authorization(data):
    """Register a parent-signed authorization."""
    auth = MedicationAuthorization(
        studentId=data.get('studentId'),
        medicationName=data.get('medicationName'),
        dosage=data.get('dosage'),
        frequency=data.get('frequency'),
        startDate=datetime.strptime(data.get('startDate'), '%Y-%m-%d').date(),
        endDate=datetime.strptime(data.get('endDate'), '%Y-%m-%d').date() if data.get('endDate') else None,
        authorizedBy=data.get('authorizedBy'),
        notes=data.get('notes'),
        isActive=True
    )
    db.session.add(auth)
    db.session.commit()
    return auth.id

def add_emergency_contact(data):
    """Add a new contact for the student."""
    contact = StudentEmergencyContact(
        studentId=data.get('studentId'),
        name=data.get('name'),
        relationship=data.get('relationship'),
        phone1=data.get('phone1'),
        phone2=data.get('phone2'),
        priority=data.get('priority', 1)
    )
    db.session.add(contact)
    db.session.commit()
    return contact.id
