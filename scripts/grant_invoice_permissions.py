from app import create_app, db
from app.models.master_scheme.screen_model import Screen
from app.models.master_scheme.roles_model import Role
from app.models.master_scheme.module_model import Module
from app.models.master_scheme.functionality_model import Functionality
from app.models.master_scheme.screen_functionality_model import ScreenFunctionality
from app.models.master_scheme.role_permission_model import RolePermission
from sqlalchemy import func as sa_func

app = create_app()

def grant_permission(role_code, screen_route, func_code, screen_name="Screen", module_name="General"):
    with app.app_context():
        try:
            # 1. Get Resources
            role = Role.query.filter_by(code=role_code).first()
            screen = Screen.query.filter_by(route=screen_route).first()
            func = Functionality.query.filter_by(code=func_code).first()

            if not role:
                print(f"❌ Role {role_code} not found")
                return

            # AUTO-CREATE SCREEN IF MISSING
            if not screen:
                print(f"⚠️ Screen {screen_route} not found. Creating it...")
                # Get Module (Financiero)
                module = Module.query.filter(Module.name.ilike(f"%{module_name}%")).first()
                if not module:
                     print(f"❌ Module {module_name} not found")
                     return
                
                # Get Max ID
                max_id = db.session.query(sa_func.max(Screen.id)).scalar() or 0
                new_id = max_id + 1
                
                print(f"✅ Found Module: {module.name} (ID: {module.id})")

                screen_code = f"SC_{screen_name.upper().replace(' ', '_')}"
                screen = Screen(
                    id=new_id,
                    name=screen_name,
                    route=screen_route,
                    code=screen_code,
                    module_id=module.id,
                    icon="fa-file-invoice-dollar",
                    order=10
                )
                db.session.add(screen)
                db.session.commit()
                print(f"✅ Created Screen {screen_name} ({screen_code}) with ID {new_id}")
            
            if not func:
                print(f"❌ Functionality {func_code} not found")
                return

            print(f"ℹ️  Processing: Role={role.name}, Screen={screen.name} ({screen.code}), Func={func.name}")

            # 2. Ensure ScreenFunctionality exists
            sf = ScreenFunctionality.query.filter_by(screen_id=screen.id, functionality_id=func.id).first()
            if not sf:
                # Get Max ID for SF
                max_sf_id = db.session.query(sa_func.max(ScreenFunctionality.id)).scalar() or 0
                new_sf_id = max_sf_id + 1

                sf = ScreenFunctionality(id=new_sf_id, screen_id=screen.id, functionality_id=func.id, is_active=True)
                db.session.add(sf)
                db.session.commit()
                print(f"✅ Created ScreenFunctionality for {screen.name} - {func.name} (ID: {new_sf_id})")
            else:
                print(f"ℹ️  ScreenFunctionality exists")

            # 3. Ensure RolePermission exists
            rp = RolePermission.query.filter_by(role_id=role.id, screen_functionality_id=sf.id).first()
            if not rp:
                rp = RolePermission(role_id=role.id, screen_functionality_id=sf.id, is_allowed=True)
                db.session.add(rp)
                db.session.commit()
                print(f"✅ Granted permission to {role.name}")
            else:
                print(f"ℹ️  Permission already granted to {role.name}")
                
            return screen.code

        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    # Grant to SYS_ADMIN
    code = grant_permission("SYS_ADMIN", "/dashboard/invoices", "CONSULTAR", "Facturas", "Financiero")
    # Ignoramos OWNER por ahora ya que no existe en DB
    if code:
        print(f"SCREEN_CODE={code}")
