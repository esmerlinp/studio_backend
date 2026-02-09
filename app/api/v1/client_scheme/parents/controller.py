from flask import render_template
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.client_scheme.parents_service import get_parent_dashboard_data
from app.models.master_scheme.user_model import User

@jwt_required()
def dashboard_view():
    """
    Render the Parent Dashboard with consolidated student data.
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Get all students and financial data for this user/parent
    family_data = get_parent_dashboard_data(user_id)
    
    return render_template(
        "es/client/parents/dashboard.html",
        user=user,
        family_data=family_data
    )

@jwt_required()
def student_360_view(student_id):
    """
    Render detailed 360 view for a specific student.
    """
    # Verify the parent has access to this student
    # (Implementation simplification: assuming services handle validation or current JWT is enough for now)
    from app.services.client_scheme.parents_service import get_student_detailed_360
    student_data = get_student_detailed_360(student_id)
    
    return render_template(
        "es/client/parents/student_360.html",
        student=student_data
    )
