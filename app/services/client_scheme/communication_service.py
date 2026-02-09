import logging
from app.models.master_scheme.user_model import User
from app.models.client_scheme.student_model import Student
from app.models.client_scheme.student_details_models import StudentFamily, StudentFamilyEmail
from app.services.client_scheme.notification_service import create_notification
from app.services.event_bus_service import event_bus, Events

logger = logging.getLogger(__name__)

def initialize_communication_subscribers():
    """
    Register subscribers to the event bus for automated communication.
    """
    event_bus.subscribe(Events.STUDENT_ATTENDANCE_ABSENT, handle_absence)
    event_bus.subscribe(Events.STUDENT_ATTENDANCE_TARDY, handle_tardiness)
    event_bus.subscribe(Events.STUDENT_HEALTH_VISIT, handle_health_visit)
    event_bus.subscribe(Events.STUDENT_CAFETERIA_PURCHASE, handle_cafeteria_purchase)
    
    logger.info("Communication subscribers initialized.")

def handle_absence(payload):
    """Notify parents about a student absence."""
    student_id = _get_student_id_from_payload(payload)
    if not student_id: return
    
    student = Student.query.get(student_id)
    parents = _get_parent_users_for_student(student_id)
    
    for parent in parents:
        create_notification(
            user_id=parent.userId,
            title="Alerta de Asistencia: Ausencia",
            message=f"Su hijo {student.firstName} ha sido marcado como AUSENTE hoy {payload.get('date')}.",
            resource_type="attendance",
            resource_id=student_id,
            target_url=f"/parents/student/{student_id}/attendance"
        )

def handle_tardiness(payload):
    """Notify parents about a student tardiness."""
    student_id = _get_student_id_from_payload(payload)
    if not student_id: return
    
    student = Student.query.get(student_id)
    parents = _get_parent_users_for_student(student_id)
    
    for parent in parents:
        create_notification(
            user_id=parent.userId,
            title="Alerta de Asistencia: Tardanza",
            message=f"Su hijo {student.firstName} llegó con TARDANZA hoy {payload.get('date')}.",
            resource_type="attendance",
            resource_id=student_id,
            target_url=f"/parents/student/{student_id}/attendance"
        )

def handle_health_visit(payload):
    """Notify parents about a nursing visit."""
    student_id = payload.get('studentId')
    student = Student.query.get(student_id)
    parents = _get_parent_users_for_student(student_id)
    
    for parent in parents:
        create_notification(
            user_id=parent.userId,
            title="Notificación de Enfermería",
            message=f"Su hijo {student.firstName} ha visitado la enfermería. Motivo: {payload.get('reason')}.",
            resource_type="health",
            resource_id=payload.get('visitId'),
            target_url=f"/parents/student/{student_id}/health"
        )

def handle_cafeteria_purchase(payload):
    """Notify parents about a cafeteria purchase (optional feedback)."""
    # This could be disabled in user preferences
    pass

# --- HELPER METHODS ---

def _get_parent_users_for_student(student_id):
    """
    Find User records associated with the student's parents/family.
    Matches emails from StudentFamilyEmail with master.usuarios.
    """
    student = Student.query.get(student_id)
    if not student or not student.familyId:
        return []
    
    family_emails = StudentFamilyEmail.query.filter_by(familyId=student.familyId).all()
    emails = [e.email for e in family_emails if e.email]
    
    if not emails:
        return []
    
    # Match against master Usuarios
    users = User.query.filter(User.email.in_(emails), User.isActive == True).all()
    return users

def _get_student_id_from_payload(payload):
    """Resolve studentId from payload, handling studentCycleClassroomId if needed."""
    if payload.get('studentId'):
        return payload.get('studentId')
    
    if payload.get('studentCycleClassroomId'):
        # Need to find the student ID from the mapping
        # Based on AttendanceListView or similar
        from app.models.client_scheme.active_cycle_student_view import ActiveCycleStudentView
        mapping = ActiveCycleStudentView.query.filter_by(
            studentCycleClassroomId=payload['studentCycleClassroomId']
        ).first()
        return mapping.studentId if mapping else None
        
    return None
