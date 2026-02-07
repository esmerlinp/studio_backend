from app import create_app, db
from app.models.master_scheme.screen_model import Screen
from app.models.master_scheme.module_model import Module
from sqlalchemy import text

app = create_app()

def generate_code(name, route):
    # Generar códigos semánticos
    # Ej: "Dashboard" -> "SC_DASHBOARD"
    # Ej: "Users" -> "SC_USERS"
    
    if "dashboard" in route:
        parts = route.strip("/").split("/")
        if len(parts) > 1:
            base = parts[1].upper().replace("-", "_")
            return f"SC_{base}"
        return "SC_DASHBOARD"
    
    # Fallback si no es una ruta de dashboard
    return f"SC_{name.upper().replace(' ', '_')}"

def migrate():
    with app.app_context():
        # 1. Crear la columna si no existe (PostgreSQL raw check)
        # Esto es solo por seguridad, idealmente ya debería estar creada por el modelo si usáramos migraciones automáticas
        try:
            db.session.execute(text('ALTER TABLE master.pantallas ADD COLUMN IF NOT EXISTS scodigo VARCHAR(50);'))
            db.session.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS uq_pantallas_scodigo ON master.pantallas(scodigo);'))
            db.session.commit()
            print("✅ Columna 'scodigo' asegurada.")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Error verificando columna: {e}")

        # 2. Popular códigos
        screens = Screen.query.all()
        updated_count = 0
        
        for screen in screens:
            if not screen.code:
                new_code = generate_code(screen.name, screen.route or "")
                
                # Check duplicados
                existing = Screen.query.filter_by(code=new_code).first()
                if existing:
                    new_code = f"{new_code}_{screen.id}"
                
                screen.code = new_code
                updated_count += 1
                print(f"🔄 Updating Screen {screen.id}: {screen.name} -> {new_code}")

        if updated_count > 0:
            db.session.commit()
            print(f"✅ {updated_count} pantallas actualizadas con código.")
        else:
            print("✨ Todas las pantallas ya tienen código.")

if __name__ == "__main__":
    migrate()
