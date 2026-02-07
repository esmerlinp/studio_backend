
from app import create_app, db
from sqlalchemy import text

app = create_app()

def fix_schema():
    with app.app_context():
        print("Applying schema fix...")
        try:
            # Create sequence
            db.session.execute(text("CREATE SEQUENCE IF NOT EXISTS master.pantallasfuncionalidades_idpantallafuncionalidad_seq;"))
            
            # Set default
            db.session.execute(text("ALTER TABLE master.pantallasfuncionalidades ALTER COLUMN idpantallafuncionalidad SET DEFAULT nextval('master.pantallasfuncionalidades_idpantallafuncionalidad_seq');"))
            
            # Associate sequence
            db.session.execute(text("ALTER SEQUENCE master.pantallasfuncionalidades_idpantallafuncionalidad_seq OWNED BY master.pantallasfuncionalidades.idpantallafuncionalidad;"))
            
            # Validar valor máximo actual
            result = db.session.execute(text("SELECT MAX(idpantallafuncionalidad) FROM master.pantallasfuncionalidades"))
            max_id = result.scalar() or 0
            
            # Set sequence value
            db.session.execute(text(f"SELECT setval('master.pantallasfuncionalidades_idpantallafuncionalidad_seq', {max_id + 1});"))
            
            db.session.commit()
            print("Schema fix applied successfully.")
            
        except Exception as e:
            print("Error applying fix:")
            print(e)
            db.session.rollback()

if __name__ == "__main__":
    fix_schema()
