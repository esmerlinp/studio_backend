from flask import Blueprint
from app.api.v1.master.auth.controller import sessions, close_session, login, logout, refresh_token, get_profile, setup_2fa, enable_2fa, disable_2fa


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/master/auth')


auth_bp.get("/sessions")(sessions)

auth_bp.put("/sessions/close/<sessionId>")(close_session)

auth_bp.post("/login")(login)
auth_bp.post("/refresh")(refresh_token)
auth_bp.post("/logout")(logout)

auth_bp.get("/profile")(get_profile)
auth_bp.post("/2fa/setup")(setup_2fa)
auth_bp.post("/2fa/enable")(enable_2fa)
auth_bp.post("/2fa/disable")(disable_2fa)


