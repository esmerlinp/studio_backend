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
