from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Check Roles
        print("--- ROLES ---")
        result = db.session.execute(text("SELECT idrol, srol, scodigo FROM master.roles"))
        for row in result:
            print(f"Role: {row[1]}, Code: {row[2]}")
            
        # Check Modules
        print("\n--- MODULES ---")
        # Check if scodigo exists in modules
        has_code_col = False
        try:
            db.session.execute(text("SELECT scodigo FROM master.modulos LIMIT 1"))
            has_code_col = True
        except:
            db.session.rollback()

        if has_code_col:
            result = db.session.execute(text("SELECT idmodulo, smodulo, scodigo FROM master.modulos"))
            for row in result:
                print(f"Module: {row[1]}, Code: {row[2]}")
        else:
            result = db.session.execute(text("SELECT idmodulo, smodulo FROM master.modulos"))
            for row in result:
                print(f"Module: {row[1]}, Code: N/A")
            
        # Check Screens
        print("\n--- SCREENS RELATED TO PARENTS/PADRES ---")
        result = db.session.execute(text("SELECT idpantalla, spantalla, scodigo, idmodulo FROM master.pantallas WHERE spantalla ILIKE '%padre%' OR spantalla ILIKE '%parent%'"))
        for row in result:
            print(f"Screen: {row[1]}, Code: {row[2]}, Module ID: {row[3]}")
            
    except Exception as e:
        print(f"Error: {e}")
