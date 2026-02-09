from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Get roles
        result = db.session.execute(text("SELECT idrol, srol, scodigo FROM master.roles"))
        print("Roles in master.roles:")
        for row in result:
            print(f"  ID: {row[0]}, Name: {row[1]}, Code: {row[2]}")
            
        # Get modules
        result = db.session.execute(text("SELECT idmodulo, smodulo FROM master.modulos"))
        print("\nModules in master.modulos:")
        for row in result:
            print(f"  ID: {row[0]}, Name: {row[1]}")
            
        # Get screens relevant to parents
        result = db.session.execute(text("SELECT idpantalla, spantalla, scodigo, sruta FROM master.pantallas WHERE spantalla ILIKE '%padre%' OR sruta ILIKE '%parents%'"))
        print("\nScreens related to parents in master.pantallas:")
        for row in result:
            print(f"  ID: {row[0]}, Name: {row[1]}, Code: {row[2]}, Route: {row[3]}")
            
    except Exception as e:
        print(f"Error: {e}")
