from flask import request
from werkzeug.security import generate_password_hash
from app.services.master_scheme import user_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity, require_role
from app.utils.responses import success, error
from app.utils.helpers import generate_reset_token, send_reset_email
from app.utils import i18n
from app.utils.helpers import send_confirmation_account_email
from uuid import uuid4

from app.services.master_scheme.user_client_service import get_client_by_user

def hashear_password(password):
    return generate_password_hash(password)



@jwt_required()
@track_activity
def me():
    user_id = get_jwt_identity()  # devuelve lo que enviaste como identity
    user = user_service.get_user_by_id(user_id=int(user_id))
    if not user:
        return success(data={}, message=i18n._("common.users.not_found"), status_code=200)
    
    return success(data=user.to_dict(), message=i18n._("common.users.retrieved_successfully"), status_code=200)



@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN"])
def get_users():
    # data = db.fetch_data('SELECT * FROM usuarios')
    user_id = get_jwt_identity()
    users = user_service.get_client_users(user_id=user_id)
    result = []
    if users:
        result = [user.to_dict() for user in users]
        #return jsonify({"result": result}), 200
    return success(data=result, message=i18n._("common.users.retrieved_successfully"), status_code=200)



@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN"])
def get_user(userId):
    user = user_service.get_user_by_id(user_id=userId)
    if not user:
        return success(data={}, message=i18n._("common.users.not_found"), status_code=200)
    
    return success(data=user.to_dict(), message=i18n._("common.users.retrieved_successfully"), status_code=200)

@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN"])
def get_user_by_name(userName):
    user = user_service.get_user_by_user_name(user_name=userName)
    if not user:
        return success(data={}, message=i18n._("common.users.not_found"), status_code=200)
    
    return success(data=user.to_dict(), message=i18n._("common.users.retrieved_successfully"), status_code=200)




@jwt_required()
@track_activity
def change_password():
    try:
        new_password = request.json.get('new_password')
        sessionId = request.json.get('sessionId')
        
        identity = get_jwt_identity()     # recupera el mismo identity guardado en el refresh token
        user = user_service.change_user_password(user_id=int(identity), new_password=new_password, sessionId=sessionId)
        if not user:
            return error(message=i18n._("common.users.not_found_or_password_not_changed"), status_code=404)

        return success(data=user.to_dict(), message=i18n._("common.auth.password_changed_successfully"), status_code=200)

        
        
    except ValueError as e:
        return error(message=e.args[0], status_code=400)
        
    except Exception as e:
        return error(message=str(e), status_code=500)
    
@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN", "ADMIN", "OWNER"])
def inactivate_user(userId):
    admin_user_id = get_jwt_identity()
    user = user_service.deactivate_user(user_id=userId, admin_user_id=admin_user_id)
    return success(data=user.to_dict())




@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN", "ADMIN", "OWNER"])
def create_user():
    try:
        admin_user_id = get_jwt_identity()
        
        username = request.json.get('userName')
        firstName = request.json.get('firstName')
        lastName = request.json.get('lastName')
        email = request.json.get('email')
       
        client = get_client_by_user(user_id=admin_user_id)
        user = user_service.insert_user(
            username=username,
            first_name=firstName,
            last_name=lastName,
            email=email,
            client_uuid=client.uuid,
            must_change_password=True
        )
        
        if user:
            #Enviar email al usuario para la activacion de la cuenta y cambio de password
            send_confirmation_account_email(user_id=user.userId, user_name=user.username, email=user.email)
            

        return success(data=user.to_dict(), message=i18n._("common.users.created_successfully"), status_code=200)

        
        
    except ValueError as e:
        return error(message=e.args[0], status_code=400)
        
    except Exception as e:
        return error(message=str(e), status_code=500)




def forgot_password():
    email = request.json.get("email")

    user = user_service.get_user_by_email(email=email)
    if not user:
        # No reveles si el usuario existe
        return success(data={}, message=i18n._("common.auth.reset_password_email_sent_if_exists"), status_code=200)

    token = generate_reset_token(user.userId)
    send_reset_email(email=user.email, token=token, userName=user.firstName)

    return success(data={}, message=i18n._("common.auth.reset_password_email_sent_if_exists"), status_code=200)








@jwt_required()
@track_activity
def update_user_preferences():
    data = request.json
    user_id = get_jwt_identity() 
    try:
        prefs = user_service.update_user_preference(
            user_id=user_id,
            language=data.get("language"),
            theme=data.get("theme"),
            timezone_=data.get("timeZone"),
            hour_format=data.get("hourFormat"),
            date_format=data.get("dateFormat"),
            receive_not_email=data.get("email"),
            push_notifications=data.get("push")
        )
        return success(prefs.to_dict())
    except Exception as e:
        return error("an error has occure")
    
@jwt_required()
@track_activity
def get_permissions():
    try:
        current_user_id = get_jwt_identity()
        client_uuid = request.args.get("client_uuid")
        module_uuid = request.args.get("module_uuid")
        screen_uuid = request.args.get("screen_uuid")
        functionality_uuid = request.args.get("functionality_uuid")
        summary = request.args.get("summary", "false").lower() == "true"

        if not client_uuid:
            return error("client_uuid is required", 400)

        # Import inside function to avoid circular imports if any
        from app.services.master_scheme.permission_service import get_user_effective_permissions

        permissions = get_user_effective_permissions(
            user_id=current_user_id,
            client_uuid=client_uuid,
            module_uuid=module_uuid,
            screen_uuid=screen_uuid,
            functionality_uuid=functionality_uuid,
            summary=summary
        )

        return success(permissions)

    except Exception as e:
        return error(str(e), 500)

@jwt_required()
@track_activity
def add_default_user_preferences():
    user_id = get_jwt_identity() 
    try:
        prefs = user_service.add_default_user_preferences(
            user_id=user_id,
        )
        return success(prefs.to_dict())
    except Exception as e:
        return error(f"an error has occure {e}")
    







# @usuarios_bp.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     conn = get_db_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute("SELECT password FROM usuarios WHERE email = %s", (data['email'],))
#     usuario = cur.fetchone()
    
#     if usuario and verificar_password(usuario['password'], data['password']):
#         return jsonify({'mensaje': 'Login exitoso'})
#     return jsonify({'error': 'Credenciales inválidas'}), 401

