from app.extensions import db
from app.models.master_scheme.attendance_type_model import AttendanceType

def get_attendance_types():
    return AttendanceType.query.all()

def get_attendance_type_by_id(at_id):
    return AttendanceType.query.get(at_id)

def create_attendance_type(data):
    at = AttendanceType(**data)
    db.session.add(at)
    db.session.commit()
    return at

def update_attendance_type(at_id, data):
    at = AttendanceType.query.get(at_id)
    if at:
        for key, value in data.items():
            setattr(at, key, value)
        db.session.commit()
    return at

def delete_attendance_type(at_id):
    at = AttendanceType.query.get(at_id)
    if at:
        db.session.delete(at)
        db.session.commit()
        return True
    return False
