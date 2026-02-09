from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Get all screens
        result = db.session.execute(text("SELECT idpantalla, spantalla, scodigo, sruta FROM master.pantallas ORDER BY idpantalla"))
        print("All Screens in master.pantallas:")
        for row in result:
            print(f"  ID: {row[0]}, Name: {row[1]}, Code: {row[2]}, Route: {row[3]}")
    except Exception as e:
        print(f"Error: {e}")
