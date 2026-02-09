from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Get function definition
        sql = text("""
            SELECT pg_get_functiondef(p.oid)
            FROM pg_proc p
            JOIN pg_namespace n ON p.pronamespace = n.oid
            WHERE n.nspname = 'cliente' AND p.proname = 'fn_permisos_usuario'
        """)
        result = db.session.execute(sql).scalar()
        print("Function definition for cliente.fn_permisos_usuario:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
