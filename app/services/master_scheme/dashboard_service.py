from app.models.master_scheme.client_model import Client
from app.models.master_scheme.plans_model import Plan
from app.models.master_scheme.price_list_model import PriceList
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from sqlalchemy import func
from app import db

def get_admin_dashboard_data():
    """
    Agrega estadísticas y datos recientes para el dashboard administrativo.
    """
    # Conteos totales
    total_clients = Client.query.count()
    active_plans = Plan.query.filter_by(is_active=True).count()
    active_price_lists = PriceList.query.filter_by(is_active=True).count()
    
    # Ingresos totales de transacciones exitosas (sumando amount)
    # Nota: Asegurarse que amount es numérico y que el filtro cubre APPROVED y SUCCESS
    total_revenue = db.session.query(func.sum(PaymentTransaction.amount))\
        .filter(PaymentTransaction.status.in_(['SUCCESS', 'APPROVED'])).scalar() or 0.0
    
    # Actividades recientes
    recent_clients = Client.query.order_by(Client.serviceStartDate.desc()).limit(5).all()
    recent_payments = PaymentTransaction.query.order_by(PaymentTransaction.createdAt.desc()).limit(5).all()
    
    
    return {
        "stats": {
            "total_clients": total_clients,
            "active_plans": active_plans,
            "active_price_lists": active_price_lists,
            "total_revenue": float(total_revenue)
        },
        "recent_clients": [c.to_dict() for c in recent_clients],
        "recent_payments": [p.to_dict() for p in recent_payments]
    }
