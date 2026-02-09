from app import db
from app.models.client_scheme.role_model import Role
from app.models.client_scheme.role_permission_model import RolePermission
from app.models.master_scheme.client_model import Client
from sqlalchemy import text

def get_roles_by_client(client_uuid: str):
    """
    Retorna los roles definidos para un cliente específico.
    """
    client = Client.query.filter_by(uuid=client_uuid).first()
    if not client:
        return []
    
    # Aquí podríamos usar set_schema si los modelos no tuvieran hardcoded 'cliente'
    # Pero siguiendo el patrón actual:
    return Role.query.all()

def create_role_for_client(client_uuid: str, data: dict):
    """
    Crea un nuevo rol en el esquema del cliente.
    """
    new_role = Role(
        name=data.get('name'),
        code=data.get('code'),
        description=data.get('description'),
        is_active=data.get('is_active', True)
    )
    db.session.add(new_role)
    db.session.commit()
    return new_role

def update_role_permissions(role_id: int, permissions: list):
    """
    Actualiza los permisos de un rol.
    'permissions' es una lista de dicts: [{'screen_functionality_id': 1, 'is_allowed': True}, ...]
    """
    # Eliminar permisos previos
    RolePermission.query.filter_by(role_id=role_id).delete()
    
    # Agregar nuevos
    for p in permissions:
        rp = RolePermission(
            role_id=role_id,
            screen_functionality_id=p['screen_functionality_id'],
            is_allowed=p.get('is_allowed', True)
        )
        db.session.add(rp)
    
    db.session.commit()
    return True

def get_role_permissions(role_id: int):
    """
    Retorna los permisos asignados a un rol.
    """
    return RolePermission.query.filter_by(role_id=role_id).all()

def get_permission_catalog():
    """
    Retorna el catálogo completo de pantallas y funcionalidades disponibles para el cliente,
    agrupadas por módulo.
    """
    sql = text("""
        SELECT 
            m.smodulo as modulo,
            m.uuidmodulo,
            p.spantalla as pantalla,
            p.uuidpantalla,
            p.scodigo as scodigopantalla,
            f.sfuncionalidad as funcionalidad,
            f.scodigo as scodigofuncionalidad,
            pf.idpantallafuncionalidad
        FROM master.modulos m
        JOIN master.pantallas p ON m.idmodulo = p.idmodulo
        JOIN master.pantallasfuncionalidades pf ON p.idpantalla = pf.idpantalla
        JOIN master.funcionalidades f ON pf.idfuncionalidad = f.idfuncionalidad
        WHERE m.bactivo = true AND p.bactivo = true AND pf.bactivo = true AND f.bactivo = true
        AND m.smodulo NOT IN ('Sistema', 'General') -- Excluir módulos administrativos de Akdmia
        ORDER BY m.iorden, p.iorden, f.sfuncionalidad
    """)
    
    result = db.session.execute(sql)
    
    catalog = {}
    for row in result:
        mod = row.modulo
        if mod not in catalog:
            catalog[mod] = {
                "name": mod,
                "uuid": str(row.uuidmodulo),
                "screens": {}
            }
        
        pantalla = row.pantalla
        if pantalla not in catalog[mod]["screens"]:
            catalog[mod]["screens"][pantalla] = {
                "name": pantalla,
                "uuid": str(row.uuidpantalla),
                "code": row.scodigopantalla,
                "functionalities": []
            }
        
        catalog[mod]["screens"][pantalla]["functionalities"].append({
            "id": row.idpantallafuncionalidad,
            "name": row.funcionalidad,
            "code": row.scodigofuncionalidad
        })
    
    # Convertir a lista para facilitar el manejo en el frontend
    flat_catalog = []
    for mod_name in catalog:
        mod_data = catalog[mod_name]
        screens_list = []
        for p_name in mod_data["screens"]:
            screens_list.append(mod_data["screens"][p_name])
        mod_data["screens"] = screens_list
        flat_catalog.append(mod_data)
        
    return flat_catalog

def get_role_users(role_id: int):
    """
    Retorna los usuarios asignados a un rol específico.
    """
    from app.models.client_scheme.user_role_model import UserRole
    from app.models.master_scheme.user_model import User
    
    user_roles = UserRole.query.filter_by(role_id=role_id, is_active=True).all()
    users = []
    for ur in user_roles:
        user = User.query.get(ur.user_id)
        if user:
            users.append({
                'id': user.userId,
                'email': user.email,
                'firstName': user.firstName,
                'lastName': user.lastName
            })
    return users

def assign_users_to_role(role_id: int, user_ids: list):
    """
    Asigna múltiples usuarios a un rol.
    """
    from app.models.client_scheme.user_role_model import UserRole
    
    # Primero, desactivar todas las asignaciones actuales
    UserRole.query.filter_by(role_id=role_id).update({'is_active': False})
    
    # Luego, activar o crear las nuevas asignaciones
    for user_id in user_ids:
        existing = UserRole.query.filter_by(role_id=role_id, user_id=user_id).first()
        if existing:
            existing.is_active = True
        else:
            new_assignment = UserRole(
                user_id=user_id,
                role_id=role_id,
                is_active=True
            )
            db.session.add(new_assignment)
    
    db.session.commit()
    return True
