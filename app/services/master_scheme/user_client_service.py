
from uuid import UUID
from app import db
from app.models.master_scheme.user_client_model import UsuarioCliente
from app.models.master_scheme.client_model import Client
from sqlalchemy.exc import IntegrityError
from typing import List

from app.utils.types import ActionType, ResourceTypes
from app import audit_log
from flask import g



def assign_user_to_client_onboard(*, user_id: int, client_uuid: str) -> UsuarioCliente:
    relation = UsuarioCliente(
        user_id=user_id,
        client_uuid=client_uuid
    )
    db.session.add(relation)
    return relation


def assign_user_to_client(
    *,
    user_id: int,
    client_uuid: str,
    commit: bool = True
) -> UsuarioCliente:

    relation = UsuarioCliente(
        user_id=user_id,
        client_uuid=client_uuid
    )

    try:
        db.session.add(relation)
        if commit:
            db.session.commit()
        else:
            db.session.flush()

        return relation

    except Exception as e:
        if commit:
            db.session.rollback()
        raise  e



# def get_client_by_userId(user_id: int) -> Client:
#     cliente = UsuarioCliente.query.filter_by(user_id=user_id).first()
#     return get_client_by_id(client_id=cliente.clientId)


@audit_log(action=ActionType.READ,
           resource_type=ResourceTypes.USER_CLIENT,
           resource_id_arg="user_id")
def get_clients_by_user(user_id: int) -> list[UsuarioCliente]:
    """
    Retorna todos los clientes a los que el usuario tiene acceso.
    """
    
    return UsuarioCliente.query.filter_by(user_id=user_id).all()

@audit_log(action=ActionType.READ,
           resource_type=ResourceTypes.USER_CLIENT,
           resource_id_arg="user_id")
def get_client_by_user(user_id: int) -> Client:
    """
    Retorna el cliente del usuario.
    """
    cliente = db.session.query(Client)\
        .join(UsuarioCliente, Client.uuid == UsuarioCliente.client_uuid)\
        .filter(UsuarioCliente.user_id == user_id)\
        .first()
        
    return cliente


@audit_log(action=ActionType.READ,
           resource_type=ResourceTypes.USER_CLIENT,
           resource_id_arg="client_uuid")
def get_users_by_client(client_uuid: UUID) -> List[UsuarioCliente]:
    """
    Retorna todos los usuarios asociados a un cliente.
    """
    return UsuarioCliente.query.filter_by(client_uuid=client_uuid).all()


@audit_log(action=ActionType.READ,
           resource_type=ResourceTypes.USER_CLIENT,
           resource_id_arg="client_uuid")
def get_user_by_client(client_uuid: UUID) -> UsuarioCliente:
    """
    Retorna el cliente del usuario.
    """
    return UsuarioCliente.query.filter_by(client_uuid=client_uuid).first()



def user_has_access_to_client(
    *,
    user_id: int,
    client_uuid: UUID
) -> bool:
    """
    Verifica si un usuario tiene acceso a un cliente.
    """
    return (
        UsuarioCliente.query
        .filter_by(user_id=user_id, client_uuid=client_uuid)
        .first()
        is not None
    )


@audit_log(action=ActionType.DELETE,
           resource_type=ResourceTypes.USER_CLIENT,
           resource_id_arg="user_id")
def remove_user_from_client(
    *,
    user_id: int,
    client_uuid: UUID
) -> bool:
    """
    Elimina la relación entre usuario y cliente.
    """
    relation = UsuarioCliente.query.filter_by(
        user_id=user_id,
        client_uuid=client_uuid
    ).first()

    if not relation:
        return False
    
    g.audit_old_values = relation.to_dict()
    
    db.session.delete(relation)
    db.session.commit()
    return True
