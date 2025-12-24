from itsdangerous import SignatureExpired, BadSignature, URLSafeTimedSerializer
from flask_mail import Message
from flask import render_template, current_app, request
from app.extensions import mail
import os
from dotenv import load_dotenv

def get_serializer():
    return URLSafeTimedSerializer(
        secret_key=current_app.config["SECRET_KEY"],
        salt="password-reset"
    )


def generate_reset_token(user_id: int) -> str:
    serializer = get_serializer()
    return serializer.dumps({"user_id": user_id})


def verify_reset_token(token: str, max_age=1800):
    serializer = get_serializer()
    try:
        data = serializer.loads(
            token,
            max_age=max_age
        )
        return data["user_id"]
    except SignatureExpired:
        return "expired"
    except BadSignature:
        return None


def send_confirmation_account_email(user_id, user_name, email):
    load_dotenv()
    token = generate_reset_token(user_id)
    confirmation_url = f"{request.host_url}/confirmation-account?token={token}"
    
    send_email_template(subject="Confirmation Account", 
                        to=[email],
                        path_template="emails/es/confirmation_email.html",
                        confirmation_url=confirmation_url, app_name=os.getenv("APP_NAME"), name=user_name
                        )
            
            
def send_reset_email(email: str, token: str, userName = ""):
    reset_url = f"{request.host_url}/reset-password?token={token}"

    msg = Message(
        subject="Cambio de contraseña",
        recipients=[email]
    )

    msg.html = render_template(
        "emails/es/reset_password_notify.html",
        reset_url=reset_url, name=userName, expiration_minutes="30"
    )

    mail.send(msg)
    
    
def send_email_template(subject:str, to:list[str], path_template, **kwargs):
 
    msg = Message(
        subject=subject,
        recipients=to
    )

    msg.html = render_template(
        path_template,
        **kwargs
    )

    mail.send(msg)
    
def send_email(subject:str, to:list[str], message):
 
    msg = Message(
        subject=subject,
        recipients=to,
        body=message
    )


    mail.send(msg)
