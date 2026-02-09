from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Get user roles and names
        sql = text("""
            SELECT u.username, r.srol, r.scodigo
            FROM master.usuarios u
            JOIN master.usuariosroles ur ON u.idusuario = ur.idusuario
            JOIN master.roles r ON ur.idrol = r.idrol
        """)
        result = db.session.execute(sql)
        print("User Roles:")
        for row in result:
            print(f"  User: {row[0]}, Role Name: {row[1]}, Role Code: {row[2]}")
            
    except Exception as e:
        print(f"Error: {e}")
