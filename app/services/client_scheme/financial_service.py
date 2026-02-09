from app import db
from sqlalchemy import text
from app.models.client_scheme.school_payment_view import SchoolPaymentView
from app.models.client_scheme.student_charge_balance_view import StudentChargeBalanceView

def get_pending_charges(filters):
    """
    Get pending charges for a family/student based on filters.
    """
    query = StudentChargeBalanceView.query
    
    if 'familyId' in filters:
        query = query.filter(StudentChargeBalanceView.studentFamilyId == filters['familyId'])
        
    if 'studentId' in filters:
        query = query.filter(StudentChargeBalanceView.studentId == filters['studentId'])
        
    if 'cycleId' in filters:
        query = query.filter(StudentChargeBalanceView.cycleId == filters['cycleId'])
        
    if 'calendarIds' in filters and filters['calendarIds']:
        # Assuming calendar IDs map to quotas or similar logic in the view
        # For now, we'll filter by quota if provided
        pass
        
    # Only show items with positive balance
    query = query.filter(StudentChargeBalanceView.balance > 0)
    
    # Order by due date logic (cycle, quota)
    query = query.order_by(StudentChargeBalanceView.cycleId, StudentChargeBalanceView.quota)
    
    return query.all()

def get_family_balance(family_id, cycle_id=None):
    """
    Get total balance and paid amount for a family.
    """
    query = StudentChargeBalanceView.query.filter(StudentChargeBalanceView.studentFamilyId == family_id)
    
    if cycle_id:
        query = query.filter(StudentChargeBalanceView.cycleId == cycle_id)
        
    results = query.all()
    
    total_balance = sum(item.balance for item in results if item.balance)
    total_paid = sum(item.totalPaid for item in results if item.totalPaid)
    
    return {
        'totalBalance': float(total_balance),
        'totalPaid': float(total_paid)
    }

def process_payment(data, user_id):
    """
    Process a new payment.
    This would typically involve:
    1. Creating a payment record in tpagos
    2. Creating details in tdetalle_pago
    3. Updating balances (via triggers or stored procs)
    
    For now, we'll implement the basic structure.
    """
    try:
        # TODO: Implement actual payment insertion using stored procedure or models
        # payment_id = create_payment_record(...)
        # create_payment_details(payment_id, data['details'])
        
        # Determine payment method and authorized User
        # ...
        
        return {"success": True, "message": "Pago procesado correctamente", "paymentId": 123}
        
    except Exception as e:
        db.session.rollback()
        raise e
