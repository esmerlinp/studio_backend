from flask import Blueprint, request
from app.utils.responses import success, error
from app.services.client_scheme.payment_calculation_service import calculate_payment_amount
from flask_jwt_extended import jwt_required

payments_bp = Blueprint('client_payments', __name__, url_prefix='/api/v1/client/payments')

@payments_bp.route("/calculate", methods=["POST"])
@jwt_required()
def calculate_payment():
    try:
        data = request.json
        required_fields = ["cycle_id", "concept_id", "base_amount", "child_number", "date_applied", "payment_frequency_id", "installment_number"]
        
        for field in required_fields:
            if field not in data:
                return error(f"Missing required field: {field}", 400)
                
        result = calculate_payment_amount(
            cycle_id=data["cycle_id"],
            concept_id=data["concept_id"],
            base_amount=data["base_amount"],
            child_number=data["child_number"],
            date_applied=data["date_applied"],
            payment_frequency_id=data["payment_frequency_id"],
            installment_number=data["installment_number"]
        )
        
        return success(result)
    except Exception as e:
        return error(str(e), 500)
