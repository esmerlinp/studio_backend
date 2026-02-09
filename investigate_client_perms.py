from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Check tables in cliente schema
        print("Tables in 'cliente' schema:")
        sql = text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'cliente' 
            AND (table_name LIKE '%rol%' OR table_name LIKE '%permiso%' OR table_name LIKE '%pantalla%')
        """)
        result = db.session.execute(sql)
        for row in result:
            print(f"  {row[0]}")
            
        # Check function definition again (full this time)
        print("\nFunction definition for cliente.fn_permisos_usuario (COMPLETE):")
        sql_fn = text("""
            SELECT pg_get_functiondef(p.oid)
            FROM pg_proc p
            JOIN pg_namespace n ON p.pronamespace = n.oid
            WHERE n.nspname = 'cliente' AND p.proname = 'fn_permisos_usuario'
        """)
        fn_def = db.session.execute(sql_fn).scalar()
        print(fn_def)
        
    except Exception as e:
        print(f"Error: {e}")
