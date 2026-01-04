from flask import Blueprint
from app.api.v1.master.notifications.controller import get_notifications, mark_read, create


notification_bp = Blueprint('notifications', __name__, url_prefix='/api/v1/user/notifications')


notification_bp.get("/")(get_notifications)

notification_bp.put("/mark_read")(mark_read)
notification_bp.post("/")(create)


