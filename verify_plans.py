from app import create_app, db
from app.models.master_scheme.plans_model import Plan
from app.models.master_scheme.price_list_model import PriceList

app = create_app()

with app.app_context():
    try:
        from flask import g
        import pytz
        g.tz = pytz.UTC
        g.date_format = "%d-%m-%Y"
        g.hour_format = "%H:%M"
        
        print("Querying plans...")
        plans = Plan.query.all()
        print(f"Found {len(plans)} plans.")
        for p in plans:
            print(f"Plan: {p.code}, ID: {p.id}")
            print("Serializing...")
            d = p.to_dict()
            print("Serialized:", d)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
