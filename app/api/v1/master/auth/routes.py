from flask import Blueprint
from app.api.v1.master.auth.controller import sessions, close_session, login, logout, refresh_token


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/master/auth')


auth_bp.get("/sessions")(sessions)

auth_bp.put("/sessions/close/<sessionId>")(close_session)

auth_bp.post("/login")(login)
auth_bp.post("/refresh")(refresh_token)
auth_bp.post("/logout")(logout)


