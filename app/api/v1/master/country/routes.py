from flask import Blueprint
from app.api.v1.master.country.controller import get_countries

countries_bp = Blueprint('countries', __name__, url_prefix='/api/v1/master/countries')

countries_bp.get("/")(get_countries)

