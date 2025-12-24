from flask import request
from app.services.client_scheme import notification_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity
from app.utils.responses import success, error
from app.utils import i18n



@jwt_required()
@track_activity
def get_notifications():
    user_id = get_jwt_identity()
    data = notification_service.get_all_notifications(user_id=user_id)
    return success(data=[notif.to_dict() for notif in data], message=i18n._("api.notifications.retrieved_successfully"), status_code=200)



@jwt_required()
@track_activity
def create():
    user_id = get_jwt_identity()
    title = request.json.get("title", None)
    message = request.json.get("message", None)
    resource_type = request.json.get("resource_type", None)
    resource_id = request.json.get("resource_id", None)
    target_url = request.json.get("target_url", None)
    
    if not title or not message:
        return error(message=i18n._("api.notifications.missing_title_or_message"), status_code=400)
    
    data = notification_service.create_notification(user_id=user_id, title=title, message=message,
    resource_type=resource_type, resource_id=resource_id, target_url=target_url)
    return success(data=data.to_dict(), message=i18n._("api.notifications.create_successfully"), status_code=200)

    
@jwt_required()
@track_activity
def mark_read():
    user_id = get_jwt_identity()
    notif_id = request.json.get("notif_id", None)
    if not notif_id:
        return error(message=i18n._("api.notifications.missing_notif_id"), status_code=400)
    
    data = notification_service.mark_read(user_id=user_id, notif_id=notif_id)
    return success(data=data.to_dict(), message=i18n._("api.notifications.marked_as_read"), status_code=200)