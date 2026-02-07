from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.master_scheme.chatbot_service import process_chat_message
from app.utils.responses import success, error
from app.utils import i18n

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/v1/master/chatbot')

@chatbot_bp.route('/query', methods=['POST'])
@jwt_required()
def chat_query():
    """
    Endpoint principal para interactuar con el chatbot.
    Recibe: { "message": "...", "history": [...] }
    Devuelve: { "response": "..." }
    """
    try:
        data = request.get_json()
        user_message = data.get('message')
        history = data.get('history', [])
        context = data.get('context', {})
        
        if not user_message:
            return error("El mensaje es requerido", 400)
            
        # Opcional: Validar permisos o registrar uso por usuario
        user_id = get_jwt_identity()
        
        response_text = process_chat_message(user_message, history, context)
        
        return success({"response": response_text})
        
    except Exception as e:
        return error(f"Error en chatbot: {str(e)}", 500)
