from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.models.client_scheme.cafeteria_models import CafeteriaProduct, StudentWallet
from app.models.client_scheme.student_model import Student
from app.models.client_scheme.student_details_models import StudentAllergy
from app.services.client_scheme.cafeteria_service import process_cafeteria_transaction

@jwt_required()
def get_pos_data():
    """Retrieve all data needed for the POS to operate offline-first or in-memory."""
    products = CafeteriaProduct.query.filter_by(isActive=True).all()
    students = Student.query.all() # In production, maybe filter by active cycle
    
    # Simple list of students with their allergies and wallet balance
    students_data = []
    for s in students:
        allergies = StudentAllergy.query.filter_by(studentId=s.id).all()
        wallet = StudentWallet.query.filter_by(studentId=s.id).first()
        students_data.append({
            "id": s.id,
            "name": f"{s.firstName} {s.lastName}",
            "code": s.studentCode,
            "allergies": [a.allergyId for a in allergies],
            "balance": float(wallet.balance) if wallet else 0
        })
        
    return jsonify({
        "products": [p.to_dict() for p in products],
        "students": students_data
    })

@jwt_required()
def checkout():
    """Process a POS transaction."""
    data = request.get_json()
    student_id = data.get('studentId')
    items = data.get('items') # List of {productId, quantity}
    payment_method = data.get('paymentMethod', 'balance')
    
    if not items:
        return jsonify({"error": "La orden está vacía"}), 400
        
    transaction_id, error_msg = process_cafeteria_transaction(student_id, items, payment_method)
    
    if error_msg:
        return jsonify({"error": error_msg}), 400
        
    return jsonify({
        "success": True,
        "transactionId": transaction_id,
        "message": "Compra procesada exitosamente"
    })
