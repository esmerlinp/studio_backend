from app.models.master_scheme.client_model import Client
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from app.models.master_scheme.user_model import User
from app.models.master_scheme.roles_model import Role
from app.models.master_scheme.screen_model import Screen
from app.models.master_scheme.functionality_model import Functionality
from app.extensions import db
from sqlalchemy import or_
from datetime import datetime

# --- Client Tools ---

def search_clients(query: str):
    """
    Busca clientes por nombre, razón social o documento.
    """
    clients = Client.query.filter(or_(
        Client.name.ilike(f'%{query}%'),
        Client.businessName.ilike(f'%{query}%'),
        Client.documentNumber.ilike(f'%{query}%')
    )).limit(5).all()
    
    return [c.to_dict() for c in clients]

def _resolve_client_id(client_identifier):
    """(Internal) Helper to resolve a client ID."""
    if isinstance(client_identifier, int) or (isinstance(client_identifier, str) and client_identifier.isdigit()):
        return int(client_identifier), None
        
    clients = search_clients(str(client_identifier))
    if not clients:
        return None, f"No encontré ningún cliente con el nombre o referencia '{client_identifier}'."
    
    return clients[0]['id'], None

def get_client_payments(client_identifier):
    """Obtiene los últimos 5 pagos de un cliente (ID o nombre)."""
    client_id, error = _resolve_client_id(client_identifier)
    if error: return {"error": error}
        
    payments = PaymentTransaction.query.filter_by(clientId=client_id).order_by(PaymentTransaction.createdAt.desc()).limit(5).all()
    result = [p.to_dict() for p in payments]
    if not result: return {"message": f"El cliente {client_identifier} no tiene pagos registrados recientes."}
    return result

def get_client_debt(client_identifier):
    """Verifica deuda/último pago de un cliente (ID o nombre)."""
    client_id, error = _resolve_client_id(client_identifier)
    if error: return {"error": error}

    last_payment = PaymentTransaction.query.filter_by(clientId=client_id).order_by(PaymentTransaction.createdAt.desc()).first()
    if not last_payment: return {"status": "No hay pagos registrados"}
    
    return {
        "last_payment_date": last_payment.paymentDate,
        "last_payment_status": last_payment.status,
        "amount": str(last_payment.amount)
    }

# --- Global System Tools ---

def get_user_info(query: str):
    """
    Busca información detallada de un usuario administrativo global por nombre, email o username.
    Retorna detalles incluyendo roles.
    """
    users = User.query.filter(or_(
        User.username.ilike(f'%{query}%'),
        User.email.ilike(f'%{query}%'),
        User.firstName.ilike(f'%{query}%'),
        User.lastName.ilike(f'%{query}%')
    )).limit(5).all()
    
    return [u.to_dict() for u in users]

def get_role_info(query: str):
    """
    Busca información sobre un Rol del sistema y sus permisos.
    """
    roles = Role.query.filter(Role.name.ilike(f'%{query}%')).limit(5).all()
    return [r.to_dict() for r in roles]

def get_screen_info(query: str):
    """
    Busca información sobre una Pantalla del sistema (módulo) y sus funcionalidades asociadas.
    """
    screens = Screen.query.filter(or_(
        Screen.name.ilike(f'%{query}%'),
        Screen.route.ilike(f'%{query}%')
    )).limit(5).all()
    
    return [s.to_dict() for s in screens]

def get_functionality_info(query: str):
    """
    Busca información de funcionalidades del sistema.
    """
    funcs = Functionality.query.filter(Functionality.name.ilike(f'%{query}%')).limit(5).all()
    return [f.to_dict() for f in funcs]

# --- Tools Map ---

TOOLS_MAP = {
    "search_clients": search_clients,
    "get_client_payments": get_client_payments,
    "get_client_debt": get_client_debt,
    "get_user_info": get_user_info,
    "get_role_info": get_role_info,
    "get_screen_info": get_screen_info,
    "get_functionality_info": get_functionality_info
}
