from app.models.client_scheme.student_charge_balance_view import StudentChargeBalanceView

def get_student_charge_balances(limit=None):
    """
    Retrieve all student charge balances.
    """
    query = StudentChargeBalanceView.query.order_by(StudentChargeBalanceView.studentName)
    if limit:
        query = query.limit(limit)
    return query.all()

def get_student_charge_balances_filtered(filters=None):
    """
    Retrieve records filtered by various criteria.
    filters: dict containing potential filter keys:
        - studentId
        - familyCode
        - cycleId
        - courseId
        - conceptId
        - isFamily
    """
    query = StudentChargeBalanceView.query
    
    if filters:
        if filters.get('studentId'):
            query = query.filter_by(studentId=filters['studentId'])
            
        if filters.get('familyCode'):
            query = query.filter_by(familyCode=filters['familyCode'])
            
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('conceptId'):
            query = query.filter_by(conceptId=filters['conceptId'])
            
        if 'isFamily' in filters:
            query = query.filter_by(isFamily=filters['isFamily'])
            
    return query.order_by(StudentChargeBalanceView.studentName).all()
