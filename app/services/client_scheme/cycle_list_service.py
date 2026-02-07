from app.models.client_scheme.cycle_list_view import CycleListView
from sqlalchemy import desc

def get_cycles(filters=None):
    """
    Retrieve cycles.
    """
    query = CycleListView.query
    
    if filters:
        if filters.get('isActive') is not None:
             query = query.filter_by(isActive=filters['isActive'])
            
    return query.order_by(desc(CycleListView.startDate)).all()

def activate_cycle(cycle_id: int):
    """
    Activates a cycle, triggering the database function to deactivate others.
    """
    from app.extensions import db
    from sqlalchemy import text
    
    # We use raw SQL because CycleListView is read-only and there is no writable Cycle model yet.
    # The trigger 'fn_ciclos_un_solo_activo' on table 'cliente.ciclos' will handle logic.
    sql = text("UPDATE cliente.ciclos SET bactivo = TRUE WHERE idciclo = :cycle_id")
    
    result = db.session.execute(sql, {'cycle_id': cycle_id})
    db.session.commit()
    
    if result.rowcount == 0:
        raise ValueError(f"Cycle with ID {cycle_id} not found.")
    
    return True
