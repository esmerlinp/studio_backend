

from app.models.client_scheme.notification_model import Notification
from typing import Optional
from ...extensions import db 
from app.utils.helpers import send_email, send_email_template
from app.services.master_scheme.user_service import get_user_preferences, get_user_by_id
from dotenv import load_dotenv
import os
from flask import request

def create_notification(
    user_id: int,
    title: str,
    message: str,
    resource_type: str,
    resource_id: int,
    action: str = "created",
    target_url: str = "/"
) -> Optional[Notification]:
    """
    Crea y persiste una notificación asociada a un recurso específico.

    Esta función se utiliza para generar notificaciones del sistema que
    permiten redirigir al usuario a un recurso concreto (por ejemplo,
    un empleado, documento o proceso) cuando interactúa con la notificación.

    Args:
        user_id (int):
            Identificador del usuario que recibirá la notificación.

        title (str):
            Título corto de la notificación.
            Ejemplo: "Empleado creado".

        message (str):
            Mensaje descriptivo de la notificación.
            Ejemplo: "El empleado Juan Pérez fue creado correctamente".

        resource_type (str):
            Tipo de recurso al que hace referencia la notificación.
            Ejemplos: "employee", "document", "payroll".

        resource_id (int):
            Identificador del recurso relacionado.
            Ejemplo: ID del empleado.

        action (str, optional):
            Acción que originó la notificación.
            Valores comunes: "created", "updated", "deleted".
            Por defecto es "created".

        target_url (str, optional):
            Ruta interna de la aplicación a la que se debe redirigir
            al usuario cuando hace click en la notificación.
            Ejemplo: "/employees/123".
            Por defecto es "/".

    Returns:
        Optional[Notification]:
            La instancia de `Notification` creada y persistida en la base
            de datos. Retorna `None` si ocurre un error durante el proceso
            (si se maneja externamente).

    Example:
        >>> create_notification(
        ...     user_id=1,
        ...     title="Empleado creado",
        ...     message="El empleado Juan Pérez fue creado correctamente",
        ...     resource_type="employee",
        ...     resource_id=123,
        ...     target_url="/employees/123"
        ... )
    """
    load_dotenv()
    notif = Notification(
        user_id=user_id,
        title=title,
        message=message,
        resource_type=resource_type,
        resource_id=resource_id,
        action=action,
        target_url=target_url
    )
    try:
        db.session.add(notif)
        db.session.commit()
        
        prefs = get_user_preferences(user_id=user_id)
        if prefs.preferences["notifications"]["email"] == True:
            user = get_user_by_id(user_id=user_id)
            
            full_url = f"{request.host_url}{target_url}"
            send_email_template(subject=title, to=[user.email], path_template="emails/es/notification_email.html",
                                title=title, message=message, target_url=full_url, app_name=os.getenv("APP_NAME"))
            

        return notif
    except Exception as e:
        db.session.rollback()
        raise e



def get_all_notifications(user_id) -> list[Optional[Notification]]:
    notifs = Notification.query.filter_by(
        user_id=user_id,
    ).order_by(Notification.created_at.desc()).all()

    return notifs


def mark_read(user_id, notif_id) -> Optional[Notification]:
    notif = Notification.query.filter_by(
        id=notif_id,
        user_id=user_id
    ).first_or_404()

    notif.read = True
    db.session.commit()

    return notif
