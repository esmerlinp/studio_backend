from flask import Blueprint
from app.api.v1.master.plan.controller import get_plans, create_plan, get_prices_list, add_price_list
from flask import request

plans_bp = Blueprint('plans', __name__, url_prefix='/api/v1/plans')



plans_bp.get("/")(get_plans)
plans_bp.get("/prices-list")(get_prices_list)
plans_bp.get("/prices-list/<int:plan_id>")(get_prices_list)

plans_bp.post("/")(create_plan)
plans_bp.post("/prices-list")(add_price_list)




