from flask import request
from werkzeug.security import generate_password_hash
from app.services import user_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity
from app.utils.responses import success, error
from app.utils.helpers import generate_reset_token, send_reset_email
from app.utils import i18n
from uuid import uuid4
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
def get_users():
    # data = db.fetch_data('SELECT * FROM usuarios')
    users = user_service.get_all_users()
    result = []
    if users:
        result = [user.to_dict() for user in users]
        #return jsonify({"result": result}), 200
    return success(data=result, message=i18n._("common.users.retrieved_successfully"), status_code=200)



@jwt_required()
@track_activity
def get_user(userId):
    user = user_service.get_user_by_id(user_id=userId)
    if not user:
        return success(data={}, message=i18n._("common.users.not_found"), status_code=200)
    
    return success(data=user.to_dict(), message=i18n._("common.users.retrieved_successfully"), status_code=200)

@jwt_required()
@track_activity
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
    





def create_user():
    try:
        
        username = request.json.get('userName')
        firstName = request.json.get('firstName')
        lastName = request.json.get('lastName')
        email = request.json.get('email')
        uuid = str(uuid4())
        password = request.json.get('password')
        
        user = user_service.insert_user(
            username=username,
            first_name=firstName,
            last_name=lastName,
            email=email,
            uuid=uuid,
            password=password,
        )

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

