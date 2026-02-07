from app.extensions import db
from sqlalchemy import text
from typing import Dict, Any, Optional
from decimal import Decimal

def calculate_payment_amount(
    cycle_id: int, 
    concept_id: int, 
    base_amount: float, 
    child_number: int, 
    date_applied: str, 
    payment_frequency_id: int, 
    installment_number: int
) -> Dict[str, Any]:
    """
    Executes cliente.fn_calcular_monto to calculate payment details.
    """
    
    sql = text("""
        SELECT * FROM cliente.fn_calcular_monto(
            :p_idciclo, 
            :p_idconcepto, 
            :p_monto_base, 
            :p_inumhijo, 
            :p_dfecha_aplica, 
            :p_idfrecuenciapago, 
            :p_inumerocuota
        )
    """)
    
    params = {
        'p_idciclo': cycle_id,
        'p_idconcepto': concept_id,
        'p_monto_base': base_amount,
        'p_inumhijo': child_number,
        'p_dfecha_aplica': date_applied,
        'p_idfrecuenciapago': payment_frequency_id,
        'p_inumerocuota': installment_number
    }
    
    try:
        result = db.session.execute(sql, params).fetchone()
        
        if result:
            return {
                "discount": float(result.ndescuento) if result.ndescuento is not None else 0.0,
                "surcharge": float(result.nrecargo) if result.nrecargo is not None else 0.0,
                "tax": float(result.nimpuesto) if result.nimpuesto is not None else 0.0,
                "total_amount": float(result.nmonto_a_pagar) if result.nmonto_a_pagar is not None else 0.0
            }
        return {} # Should not happen given function returns 1 row
        
    except Exception as e:
        raise e
