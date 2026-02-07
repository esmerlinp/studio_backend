import google.generativeai as genai
import os
from .chatbot_tools import TOOLS_MAP
from dotenv import load_dotenv
from flask import current_app

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_model():
    """
    Inicializa y devuelve el modelo configurado con las herramientas.
    """
    tools_list = list(TOOLS_MAP.values())
    return genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        tools=tools_list
    )

def process_chat_message(user_message: str, history: list = None, context: dict = None):
    """
    Procesa un mensaje del usuario, maneja el historial, ejecuta herramientas y utiliza el contexto de la página.
    """
    if history is None:
        history = []

    # 1. Preparar historial para la API de Gemini
    chat_history = []
    for msg in history:
        role = 'user' if msg.get('role') == 'user' else 'model'
        content = msg.get('content', '')
        chat_history.append({
            "role": role,
            "parts": [content]
        })

    try:
        model = get_model()
        chat = model.start_chat(history=chat_history, enable_automatic_function_calling=True)
        
        # 2. Construir el mensaje con contexto si existe
        if context:
            # Filtramos contenido muy largo o irrelevante si es necesario
            context_str = f"""
[CONTEXTO DE LA PANTALLA ACTUAL]
El usuario está viendo la siguiente página en el dashboard administrativo:
- Título: {context.get('title', 'N/A')}
- URL: {context.get('url', 'N/A')}

Contenido de texto visible:
{context.get('content', '')[:3000]}

Datos de formularios detectados:
{context.get('formData', {})}

[INSTRUCCIÓN DEL SISTEMA]
Actúas como un Asistente Global del Sistema "Akdmia Studio".
TIENES ACCESO A TODA LA BASE DE DATOS del sistema a través de tus herramientas (Usuarios, Roles, Pantallas, Clientes, Pagos, etc.).
- Si el usuario pregunta algo específico de la pantalla actual (ej: "este cliente", "este formulario"), USA EL CONTEXTO DE PANTALLA.
- Si el usuario pregunta algo general o busca datos no visibles (ej: "¿Quién es el usuario X?", "Busca la pantalla Y"), USA TUS HERRAMIENTAS GLOBALES.
- NO te limites al contexto de la pantalla si la respuesta requiere buscar en la base de datos global.
[FIN INSTRUCCIÓN]

Consulta del usuario: {user_message}
"""
            message_to_send = context_str
        else:
            message_to_send = user_message

        # 3. Enviar mensaje
        response = chat.send_message(message_to_send)
        
        return response.text
        
    except Exception as e:
        current_app.logger.error(f"Error en Chatbot Service: {str(e)}")
        return "Lo siento, hubo un error al procesar tu solicitud. Por favor intenta de nuevo."
