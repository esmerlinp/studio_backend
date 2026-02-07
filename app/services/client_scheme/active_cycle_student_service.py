from app import db
from app.models.client_scheme.active_cycle_student_view import ActiveCycleStudentView
from app.models.client_scheme.student_list_view import StudentListView

def get_active_cycle_students():
    """
    Retrieve all active cycle students.
    """
    return ActiveCycleStudentView.query.order_by(ActiveCycleStudentView.studentName).all()

def get_active_cycle_students_filtered(filters=None):
    """
    Retrieve records filtered by various criteria.
    Joins with StudentListView to get responsible information.
    Returns a query with explicit columns to ensure JSON serializability.
    """
    query = db.session.query(
        ActiveCycleStudentView.studentCycleClassroomId,
        ActiveCycleStudentView.studentCode,
        ActiveCycleStudentView.studentName,
        ActiveCycleStudentView.courseName,
        ActiveCycleStudentView.classroomName,
        ActiveCycleStudentView.studentStatus,
        StudentListView.responsibleName,
        StudentListView.responsiblePhone,
        ActiveCycleStudentView.studentId
    ).outerjoin(
        StudentListView, 
        ActiveCycleStudentView.studentCycleClassroomId == StudentListView.studentClassroomCycleId
    )
    
    if filters:
        if filters.get('studentId'):
            query = query.filter(ActiveCycleStudentView.studentId == filters['studentId'])
            
        if filters.get('courseId'):
            query = query.filter(ActiveCycleStudentView.courseId == filters['courseId'])
            
        if filters.get('levelId'):
            query = query.filter(ActiveCycleStudentView.levelId == filters['levelId'])
            
        if filters.get('cycleId'):
            query = query.filter(ActiveCycleStudentView.cycleId == filters['cycleId'])
            
        if filters.get('search'):
            search_term = f"%{filters['search']}%"
            query = query.filter(
                (ActiveCycleStudentView.studentName.ilike(search_term)) |
                (ActiveCycleStudentView.studentCode.ilike(search_term))
            )
            
    return query.order_by(ActiveCycleStudentView.studentName)
