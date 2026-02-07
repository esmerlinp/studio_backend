from app import create_app, db
from app.models.master_scheme.screen_model import Screen
from app.models.master_scheme.roles_model import Role
from app.models.master_scheme.module_model import Module
from app.models.master_scheme.functionality_model import Functionality
from app.models.master_scheme.screen_functionality_model import ScreenFunctionality
from app.models.master_scheme.role_permission_model import RolePermission
from sqlalchemy import func as sa_func

app = create_app()

# MAP: Route -> (ScreenName, ModuleName, FunctionalityCode)
# Assuming 'CONSULTAR' for all GET dashboard routes
ROUTE_MAP = {
    "/dashboard/price-lists": ("Listas de Precios", "Financiero", "CONSULTAR"),
    "/dashboard/payments": ("Pagos", "Financiero", "CONSULTAR"),
    "/dashboard/ncf": ("Secuencias NCF", "Financiero", "CONSULTAR"),
    "/dashboard/ncf/logs": ("Logs NCF", "Financiero", "CONSULTAR"),
    "/dashboard/allergies": ("Alergias", "Enfermería", "CONSULTAR"),
    "/dashboard/banks": ("Bancos", "Financiero", "CONSULTAR"),
    "/dashboard/cities": ("Ciudades", "General", "CONSULTAR"), # General module?
    "/dashboard/marital-status": ("Estados Civiles", "General", "CONSULTAR"),
    "/dashboard/functionalities": ("Funcionalidades", "Sistema", "CONSULTAR"),
    "/dashboard/modules": ("Módulos", "Sistema", "CONSULTAR"),
    "/dashboard/users": ("Usuarios", "General", "CONSULTAR"), # Assuming users is general
    "/dashboard/screens": ("Pantallas", "Sistema", "CONSULTAR"),
    "/dashboard/professions": ("Profesiones", "General", "CONSULTAR"),
    "/dashboard/user_sessions": ("Sesiones", "Sistema", "CONSULTAR"), 
    "/dashboard/currencies": ("Monedas", "Financiero", "CONSULTAR"),
    "/dashboard/month-names": ("Nombres de Meses", "General", "CONSULTAR"),
    "/dashboard/weekday-names": ("Nombres de Días", "General", "CONSULTAR"),
    "/dashboard/other-schools": ("Otras Escuelas", "Académico", "CONSULTAR"),
    "/dashboard/functions": ("Funciones", "Sistema", "CONSULTAR"),
    "/dashboard/medical_institutions": ("Instituciones Médicas", "Enfermería", "CONSULTAR"),
    "/dashboard/health_insurance_institutions": ("ARS", "Financiero", "CONSULTAR"), # Actually Seguro Medico
    "/dashboard/screens": ("Pantallas", "Sistema", "CONSULTAR"),
    "/dashboard/screen-functionalities": ("Funcionalidades Pantalla", "Sistema", "CONSULTAR"),
    "/dashboard/payment-processors": ("Procesadores de Pago", "Financiero", "CONSULTAR"),
    "/dashboard/role-permissions": ("Permisos de Roles", "Sistema", "CONSULTAR"),
    "/dashboard/genders": ("Géneros", "General", "CONSULTAR"),
    "/dashboard/attendance-types": ("Tipos de Asistencia", "Académico", "CONSULTAR"),
    "/dashboard/document-types": ("Tipos de Documento", "General", "CONSULTAR"),
    "/dashboard/blood-types": ("Tipos de Sangre", "Enfermería", "CONSULTAR"),
    "/dashboard/phone-types": ("Tipos de Teléfono", "General", "CONSULTAR"),
    "/dashboard/roles-master": ("Roles", "Sistema", "CONSULTAR"),
    "/dashboard/user-roles": ("Roles de Usuario", "Sistema", "CONSULTAR"),
    "/dashboard/sectors": ("Sectores", "General", "CONSULTAR"),
    "/dashboard/clients": ("Clientes", "General", "CONSULTAR"),
    "/dashboard/price-lists": ("Listas de Precios", "Financiero", "CONSULTAR"),
    "/dashboard/plans": ("Planes", "Financiero", "CONSULTAR"),
    "/dashboard/invoices": ("Facturas", "Financiero", "CONSULTAR"),
}

def grant_permission(role_code, screen_route, func_code, screen_name, module_name):
    with app.app_context():
        try:
            role = Role.query.filter_by(code=role_code).first()
            func = Functionality.query.filter_by(code=func_code).first()
            screen = Screen.query.filter_by(route=screen_route).first()

            if not role: return print(f"❌ Role {role_code} not found")
            if not func: return print(f"❌ Functionality {func_code} not found")

            # GET OR CREATE MODULE
            module = Module.query.filter(Module.name.ilike(f"%{module_name}%")).first()
            if not module:
                # Fallback to General/System if specified doesn't exist, or create temp
                module = Module.query.filter(Module.name.ilike("%General%")).first()
                if not module:
                     module = Module(name=module_name, description="Auto-created", icon="fa-cube", order=99)
                     db.session.add(module)
                     db.session.flush()

            # GET OR CREATE SCREEN
            if not screen:
                screen_code = f"SC_{screen_name.upper().replace(' ', '_')}"
                # Get Max ID for Screen
                max_id = db.session.query(sa_func.max(Screen.id)).scalar() or 0
                new_id = max_id + 1
                
                screen = Screen(
                    id=new_id,
                    name=screen_name,
                    route=screen_route,
                    code=screen_code,
                    module_id=module.id,
                    icon="fa-circle", 
                    order=99
                )
                db.session.add(screen)
                db.session.commit()
                print(f"✅ Created Screen {screen_name} ({screen_code})")
            
            # ENSURE SF
            sf = ScreenFunctionality.query.filter_by(screen_id=screen.id, functionality_id=func.id).first()
            if not sf:
                max_sf_id = db.session.query(sa_func.max(ScreenFunctionality.id)).scalar() or 0
                sf = ScreenFunctionality(id=max_sf_id+1, screen_id=screen.id, functionality_id=func.id, is_active=True)
                db.session.add(sf)
                db.session.commit()
            
            # ENSURE PERMISSION
            rp = RolePermission.query.filter_by(role_id=role.id, screen_functionality_id=sf.id).first()
            if not rp:
                rp = RolePermission(role_id=role.id, screen_functionality_id=sf.id, is_allowed=True)
                db.session.add(rp)
                db.session.commit()
                print(f"✅ Granted {role.name} -> {screen_name}")
            else:
                print(f"ℹ️  {role.name} already has {screen_name}")

            return screen.code

        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Error {screen_route}: {e}")

if __name__ == "__main__":
    for route, (name, mod, func) in ROUTE_MAP.items():
        grant_permission("SYS_ADMIN", route, func, name, mod)
        # grant_permission("OWNER", route, func, name, mod) # Owner not in DB yet
