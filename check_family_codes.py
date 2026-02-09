from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Get some family codes
        result = db.session.execute(text("SELECT idestudiantefam, scodfam FROM cliente.estudiantesfam LIMIT 10"))
        print("Family Codes (scodfam) in cliente.estudiantesfam:")
        for row in result:
            print(f"  ID: {row[0]}, Code: {row[1]}")
            
    except Exception as e:
        print(f"Error: {e}")
