from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Get screens in module 4 (Padres)
        result = db.session.execute(text("SELECT idpantalla, spantalla, scodigo, sruta FROM master.pantallas WHERE idmodulo = 4"))
        print("Screens in Padres module (ID 4):")
        found_any = False
        for row in result:
            found_any = True
            print(f"  ID: {row[0]}, Name: {row[1]}, Code: {row[2]}, Route: {row[3]}")
            
        if not found_any:
            print("  No screens found explicitly linked to module 4.")
            
        # Also check functionalities for these screens
        result = db.session.execute(text("""
            SELECT p.spantalla, f.scodigo 
            FROM master.pantallas p
            JOIN master.pantallasfuncionalidades pf ON p.idpantalla = pf.idpantalla
            JOIN master.funcionalidades f ON pf.idfuncionalidad = f.idfuncionalidad
            WHERE p.idmodulo = 4
        """))
        print("\nFunctionalities for Padres screens:")
        for row in result:
            print(f"  Screen: {row[0]}, Functionality Code: {row[1]}")

        # Check for any screen with PADRE in name regardless of module
        result = db.session.execute(text("SELECT idpantalla, spantalla, scodigo, idmodulo FROM master.pantallas WHERE spantalla ILIKE '%padre%'"))
        print("\nScreens with 'Padre' in name (any module):")
        for row in result:
            print(f"  ID: {row[0]}, Name: {row[1]}, Code: {row[2]}, Module ID: {row[3]}")
            
    except Exception as e:
        print(f"Error: {e}")
