from app.models.client_scheme.formula_list_view import FormulaListView

def get_formulas(filters=None):
    """
    Retrieve formulas.
    """
    query = FormulaListView.query
    
    if filters:
        if filters.get('isActive') is not None:
             query = query.filter_by(isActive=filters['isActive'])
            
    return query.order_by(FormulaListView.description).all()
