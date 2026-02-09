from typing import List, Dict, Any
from app.services.master_scheme.permission_service import get_user_effective_permissions

def get_user_menu_items(user_id: int, client_uuid: str, module: str) -> List[Dict[str, Any]]:
    """
    Returns the menu items a user can see for a specific module based on their permissions.
    This ensures role isolation - users only see what they have access to.
    
    Special cases:
    - Users with srol='OWNER' or 'ROOT' see all menu items
    """
    
    # Define all possible menu items per module with their required permission
    menu_definitions = {
        'academic': [
            {'label': 'Dashboard', 'url': '/client/dashboard', 'icon': 'fa-home', 'screen': 'SC_DASHBOARD_ACADÉMICO', 'func': 'CONSULTAR'},
            {'label': 'Estudiantes', 'url': '/client/students', 'icon': 'fa-users', 'screen': 'SC_EXPEDIENTE_DE_ESTUDIANTE', 'func': 'CONSULTAR'},
            {'label': 'Admisiones', 'url': '/client/admissions', 'icon': 'fa-user-plus', 'screen': 'SC_SOLICITUD_DE_ADMISIÓN', 'func': 'CONSULTAR'},
            {'label': 'Asistencia', 'url': '/client/attendance', 'icon': 'fa-calendar-check', 'screen': 'SC_ASISTENCIA', 'func': 'CONSULTAR'},
            {'label': 'Notas', 'url': '/client/grades', 'icon': 'fa-clipboard-list', 'screen': 'SC_DIGITACIÓN_DE_NOTAS', 'func': 'CONSULTAR'},
            {'label': 'Asignación de Aulas', 'url': '/client/classroom-assignment', 'icon': 'fa-chalkboard-teacher', 'screen': 'SC_ASIGNACIÓN_DE_AULAS', 'func': 'CONSULTAR'},
            {'label': 'Configuración', 'url': '/client/configuration', 'icon': 'fa-cog', 'screen': 'SC_CICLOS_ESCOLARES_-_MÓDULO_ACADÉMICO', 'func': 'CONSULTAR'},
        ],
        'finance': [
            {'label': 'Dashboard Financiero', 'url': '/client/financial', 'icon': 'fa-chart-line', 'screen': 'SC_DASHBOARD_FINANCIERO', 'func': 'CONSULTAR'},
            {'label': 'Pagos', 'url': '/client/financial/payments', 'icon': 'fa-money-bill-wave', 'screen': 'SC_PAGOS', 'func': 'CONSULTAR'},
        ],
        'health': [
            {'label': 'Dashboard Enfermería', 'url': '/client/health', 'icon': 'fa-heartbeat', 'screen': 'SC_ENFERMERIA_DASHBOARD', 'func': 'CONSULTAR'},
            {'label': 'Visitas Médicas', 'url': '/client/health/visits', 'icon': 'fa-notes-medical', 'screen': 'SC_ENFERMERIA_VISITAS', 'func': 'CONSULTAR'},
            {'label': 'Inventario Médico', 'url': '/client/health/inventory', 'icon': 'fa-pills', 'screen': 'SC_ENFERMERIA_INVENTARIO', 'func': 'CONSULTAR'},
        ],
        'parents': [
            {'label': 'Mi Dashboard', 'url': '/client/parents', 'icon': 'fa-home', 'screen': 'SC_PADRES_DASHBOARD', 'func': 'CONSULTAR'},
            {'label': 'Expediente 360', 'url': '/client/parents/student', 'icon': 'fa-user-graduate', 'screen': 'SC_PADRES_STUDENT_360', 'func': 'CONSULTAR'},
        ],
        'cafeteria': [
            {'label': 'Dashboard Cafetería', 'url': '/client/cafeteria', 'icon': 'fa-utensils', 'screen': 'SC_CAFETERIA_DASHBOARD', 'func': 'CONSULTAR'},
            {'label': 'Punto de Venta', 'url': '/client/cafeteria/pos', 'icon': 'fa-cash-register', 'screen': 'SC_CAFETERIA_POS', 'func': 'CONSULTAR'},
            {'label': 'Productos', 'url': '/client/cafeteria/items', 'icon': 'fa-hamburger', 'screen': 'SC_CAFETERIA_ITEMS', 'func': 'CONSULTAR'},
            {'label': 'Órdenes', 'url': '/client/cafeteria/orders', 'icon': 'fa-receipt', 'screen': 'SC_CAFETERIA_ORDERS', 'func': 'CONSULTAR'},
        ]
    }
    
    if module not in menu_definitions:
        return []
    
    # Check if user is OWNER or ROOT - they see everything
    from app.models.master_scheme.user_model import User
    user = User.query.get(user_id)
    if user and user.rol in ['OWNER', 'ROOT']:
        # Return all menu items for this module
        return [
            {
                'label': item['label'],
                'url': item['url'],
                'icon': item['icon']
            }
            for item in menu_definitions[module]
        ]
    
    # Get all user permissions for this client
    permissions = get_user_effective_permissions(
        user_id=user_id,
        client_uuid=client_uuid
    )
    
    # Create a set of allowed screen+functionality combinations
    allowed_perms = set()
    for perm in permissions:
        if perm.get('bpermitido'):
            screen_code = perm.get('scodigopantalla')
            func_code = perm.get('scodigofuncionalidad')
            if screen_code and func_code:
                allowed_perms.add(f"{screen_code}|{func_code}")
    
    # Filter menu items based on permissions
    visible_items = []
    for item in menu_definitions[module]:
        perm_key = f"{item['screen']}|{item['func']}"
        if perm_key in allowed_perms:
            visible_items.append({
                'label': item['label'],
                'url': item['url'],
                'icon': item['icon']
            })
    
    return visible_items
