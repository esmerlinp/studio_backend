from app.models.client_scheme.current_tax_view import CurrentTaxView

def get_current_tax():
    """
    Retrieve the current active tax.
    Since the view limits to 1, we can return the first result.
    """
    return CurrentTaxView.query.first()
