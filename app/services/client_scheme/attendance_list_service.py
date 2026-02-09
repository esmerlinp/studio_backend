from app.models.client_scheme.attendance_list_view import AttendanceListView
from app.models.client_scheme.active_cycle_student_view import ActiveCycleStudentView
from app.models.client_scheme.attendance_model import Attendance
from app import db
from sqlalchemy import desc, and_
from datetime import datetime

def get_attendances(filters=None):
    """
    Retrieve attendances.
    """
    query = AttendanceListView.query
    
    if filters:
        if filters.get('studentId'):
            query = query.filter_by(studentId=filters['studentId'])
            
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('date'):
            query = query.filter_by(date=filters['date'])
            
    return query.order_by(desc(AttendanceListView.date)).all()

def get_attendance_checklist(filters):
    """
    Retrieve students for a specific class and their attendance for a given date.
    filters: 
        - date (required)
        - levelId (optional)
        - courseId (optional)
        - classroomId (optional)
    """
    date_str = filters.get('date')
    if not date_str:
        return []
    
    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Base query for students in the active cycle
    student_query = ActiveCycleStudentView.query
    
    if filters.get('levelId'):
        student_query = student_query.filter_by(levelId=filters['levelId'])
    if filters.get('courseId'):
        student_query = student_query.filter_by(courseId=filters['courseId'])
    if filters.get('classroomId'):
        student_query = student_query.filter_by(classroomId=filters['classroomId'])
        
    students = student_query.all()
    
    # Get existing attendance records for the same filters and date
    student_ids = [s.studentCycleClassroomId for s in students]
    if not student_ids:
        return []

    attendance_query = Attendance.query.filter(
        Attendance.date == target_date,
        Attendance.studentCycleClassroomId.in_(student_ids)
    )
    existing_attendances = {a.studentCycleClassroomId: a for a in attendance_query.all()}
    
    checklist = []
    for s in students:
        att = existing_attendances.get(s.studentCycleClassroomId)
        checklist.append({
            "studentCycleClassroomId": s.studentCycleClassroomId,
            "studentId": s.studentId,
            "studentCode": s.studentCode,
            "studentName": s.studentName,
            "courseName": s.courseName,
            "classroomName": s.classroomName,
            "attendanceId": att.attendanceId if att else None,
            "attendanceTypeId": att.attendanceTypeId if att else None,
            "comment": att.comment if att else ""
        })
        
    return checklist

def save_bulk_attendance(data):
    """
    Save or update multiple attendance records.
    data: list of dicts {studentCycleClassroomId, date, attendanceTypeId, comment}
    """
    results = []
    for item in data:
        student_cycle_classroom_id = item.get('studentCycleClassroomId')
        date_str = item.get('date')
        attendance_type_id = item.get('attendanceTypeId')
        comment = item.get('comment', '')
        
        if not student_cycle_classroom_id or not date_str or not attendance_type_id:
            continue
            
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Check if record exists
        att = Attendance.query.filter_by(
            studentCycleClassroomId=student_cycle_classroom_id,
            date=target_date
        ).first()
        
        if att:
            # Update
            old_type = att.attendanceTypeId
            att.attendanceTypeId = attendance_type_id
            att.comment = comment
            
            # Emit if status changed to critical
            if old_type != attendance_type_id:
                _emit_attendance_event(att)
        else:
            # Create
            att = Attendance(
                studentCycleClassroomId=student_cycle_classroom_id,
                date=target_date,
                attendanceTypeId=attendance_type_id,
                comment=comment
            )
            db.session.add(att)
            _emit_attendance_event(att)
            
        results.append(att)
        
    db.session.commit()
    return results

def _emit_attendance_event(attendance):
    """Internal helper to emit event based on type."""
    from app.services.event_bus_service import emit_event, Events
    
    # 2 = Absent, 3 = Tardy
    if attendance.attendanceTypeId == 2:
        emit_event(Events.STUDENT_ATTENDANCE_ABSENT, {
            "studentCycleClassroomId": attendance.studentCycleClassroomId,
            "date": attendance.date.isoformat()
        })
    elif attendance.attendanceTypeId == 3:
        emit_event(Events.STUDENT_ATTENDANCE_TARDY, {
            "studentCycleClassroomId": attendance.studentCycleClassroomId,
            "date": attendance.date.isoformat()
        })
