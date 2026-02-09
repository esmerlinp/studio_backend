from app.extensions import db
from sqlalchemy import text
from typing import List, Optional, Dict, Any

def get_user_effective_permissions(
    user_id: int, 
    client_uuid: str, 
    module_uuid: Optional[str] = None, 
    screen_uuid: Optional[str] = None, 
    functionality_uuid: Optional[str] = None, 
    summary: bool = False
) -> List[Dict[str, Any]]:
    """
    Executes cliente.fn_permisos_usuario to get effective permissions for a user in a client.
    """
    
    sql = text("""
        SELECT * FROM cliente.fn_permisos_usuario(
            :p_idusuario, 
            :p_uuidcliente, 
            :p_uuidmodulo, 
            :p_uuidpantalla, 
            :p_uuidfuncionalidad, 
            :p_bresumenmodulos
        )
    """)
    
    params = {
        'p_idusuario': user_id,
        'p_uuidcliente': client_uuid,
        'p_uuidmodulo': module_uuid,
        'p_uuidpantalla': screen_uuid,
        'p_uuidfuncionalidad': functionality_uuid,
        'p_bresumenmodulos': summary
    }
    
    try:
        result = db.session.execute(sql, params)
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]
    except Exception as e:
        # Log error or re-raise
        raise e

def check_user_permission(user_id: int, client_uuid: str, screen_code: str, functionality_code: str) -> bool:
    """
    Checks if a user has a specific permission in a client context using semantic codes.
    Strictly isolates permissions to the provided client_uuid.
    
    Special cases:
    - Users with srol='OWNER' or 'ROOT' in master.usuarios have automatic full access
    """
    try:
        # Check if user is OWNER or ROOT - they have automatic full access
        from app.models.master_scheme.user_model import User
        user = User.query.get(user_id)
        if user and user.rol in ['OWNER', 'ROOT']:
            return True
        
        # We call the effective permissions for the specific user and client
        permissions = get_user_effective_permissions(
            user_id=user_id,
            client_uuid=client_uuid
        )
        
        # Search for the specific matching screen and functionality code
        for perm in permissions:
            # The column in DB is now 'scodigopantalla' (returned by fn_permisos_usuario)
            if (perm.get('scodigopantalla') == screen_code and 
                perm.get('scodigofuncionalidad') == functionality_code):
                return bool(perm.get('bpermitido', False))
        
        return False
    except Exception as e:
        # In case of error, default to no permission and log it
        from flask import current_app
        current_app.logger.error(f"Permission check failed for user {user_id}, client {client_uuid}: {str(e)}")
        return False
