
from app.utils.responses import success, error
from app.models.master_scheme.country_model import Country
from app import limiter


@limiter.limit("30 per minute")
def get_countries():
    data = Country.query.filter_by(is_active = True).all()
    return success(data=[notif.to_dict() for notif in data])