from app import create_app
from app.models.master_scheme.screen_model import Screen
from app.models.master_scheme.module_model import Module

app = create_app()
with app.app_context():
    # Find module
    m = Module.query.filter(Module.name.ilike('%padre%')).first()
    if m:
        print(f"Module: {m.name}, ID: {m.id}")
        screens = Screen.query.filter_by(module_id=m.id).all()
        for s in screens:
            print(f"  Screen: {s.name}, Code: {s.code}, Route: {s.route}")
    else:
        print("Module 'Padres' not found by name.")
        # Search all screens
        screens = Screen.query.filter(Screen.name.ilike('%padre%')).all()
        for s in screens:
            print(f"Screen: {s.name}, Code: {s.code}, Route: {s.route}")
