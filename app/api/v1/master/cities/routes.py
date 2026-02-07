from flask import Blueprint
from . import controller

cities_bp = Blueprint('cities', __name__, url_prefix='/api/v1/master/cities')

cities_bp.get("/")(controller.get_cities)
cities_bp.get("/<int:city_id>")(controller.get_city)
cities_bp.post("/")(controller.create_city)
cities_bp.put("/<int:city_id>")(controller.update_city)
cities_bp.delete("/<int:city_id>")(controller.delete_city)
