from app.models.client_scheme.student_model import Student
from app.models.client_scheme.student_details_models import StudentFamily, StudentFamilyEmail
from app.models.client_scheme.nursing_models import NursingVisit, StudentCondition
from app.models.client_scheme.cafeteria_models import StudentWallet, StudentDietaryRestriction
from app.models.client_scheme.attendance_list_view import AttendanceListView
from app.services.client_scheme.financial_service import get_family_balance

def get_parent_dashboard_data(user_id):
    """
    Consolidate all relevant data for a parent's dashboard.
    1. Find family associated with User's email.
    2. Find all students in that family.
    3. Get 360 view for each student.
    """
    from app.models.master_scheme.user_model import User
    user = User.query.get(user_id)
    if not user: return None
    
    # 1. Find family by email
    family_email = StudentFamilyEmail.query.filter_by(email=user.email).first()
    if not family_email:
        return {"error": "No se encontró familia asociada a este usuario."}
    
    family_id = family_email.familyId
    students = Student.query.filter_by(familyId=family_id).all()
    
    # 2. Financial Summary
    financial_summary = get_family_balance(family_id)
    
    # 3. Students Details
    students_data = []
    for s in students:
        # Health critical check
        critical_conditions = StudentCondition.query.filter_by(studentId=s.id, isCritical=True).all()
        
        # Recent attendance
        recent_attendance = AttendanceListView.query.filter_by(studentId=s.id).order_by(AttendanceListView.date.desc()).limit(5).all()
        
        # Wallet
        wallet = StudentWallet.query.filter_by(studentId=s.id).first()
        
        students_data.append({
            "id": s.id,
            "fullName": f"{s.firstName} {s.lastName}",
            "studentCode": s.studentCode,
            "photoUrl": s.photoUrl,
            "health": {
                "hasCriticalConditions": len(critical_conditions) > 0,
                "conditionsCount": StudentCondition.query.filter_by(studentId=s.id).count()
            },
            "attendance": [
                {"date": a.date.isoformat() if a.date else None, "type": a.attendanceTypeName} 
                for a in recent_attendance
            ],
            "wallet": {
                "balance": float(wallet.balance) if wallet and wallet.balance is not None else 0,
                "isActive": wallet.isActive if wallet else False
            }
        })
        
    return {
        "familyId": family_id,
        "financialSummary": financial_summary,
        "students": students_data
    }

def get_student_detailed_360(student_id):
    """Deep dive into a single student's status for the Parent Portal."""
    student = Student.query.get(student_id)
    if not student: return None
    
    # Fetch all modules data
    wallet = StudentWallet.query.filter_by(studentId=student_id).first()
    restrictions = StudentDietaryRestriction.query.filter_by(studentId=student_id).first()
    conditions = StudentCondition.query.filter_by(studentId=student_id).all()
    recent_visits = NursingVisit.query.filter_by(studentId=student_id).order_by(NursingVisit.date.desc()).limit(10).all()
    
    return {
        "profile": student.to_dict(include_sensitive=True),
        "health": {
            "conditions": [c.to_dict() for c in conditions],
            "recentVisits": [v.to_dict() for v in recent_visits]
        },
        "cafeteria": {
            "balance": float(wallet.balance) if wallet and wallet.balance is not None else 0,
            "restrictions": restrictions.to_dict() if restrictions else None
        }
    }
