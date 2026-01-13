from google import genai
import os
from google.api_core import exceptions

# Configura tu llave de API
client = genai.Client(api_key="AIzaSyALDyvLZU7FUfj1H3u1J8pvXVqiFkPK9VQ")

def generar_reporte_estudiante(datos_estudiante):
    """
    Envía los datos del estudiante a Gemini para generar un análisis detallado.
    """
    try:
        # El 'Prompt' es la instrucción que le damos a la IA
        prompt = f"""
        Actúa como un psicopedagogo experto. Analiza los siguientes datos del estudiante en Akdmia:
        
        DATOS:
        - Calificaciones: {datos_estudiante['notas']}
        - Hábitos Alimenticios: {datos_estudiante['comida']}
        - Tareas Recientes: {datos_estudiante['tareas']}
        
        PROPORCIONA:
        1. Resumen del comportamiento general.
        2. Relación entre alimentación y rendimiento (si aplica).
        3. Tres puntos específicos a mejorar basados en sus tareas y notas.
        4. Un mensaje motivacional corto para el estudiante.
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash", # El modelo más rápido y eficiente para reportes
            #model="gemini-1.5-flash",
            #model="gemini-1.5-flash-latest",  # Agrega '-latest'
            contents=prompt
        )

        return response.text
    except exceptions.ResourceExhausted as e:
        # Error de cuota (muy común en Gemini Free)
        error_msg = "Se ha agotado el límite de peticiones gratuitas. Reintenta en un minuto."
        return {"error": error_msg}, 429

    except Exception as e:
        # Error genérico: Convertimos el error a STRING para evitar el problema del 'set'
        error_str = str(e)
        return {"error": f"Error interno del servidor {error_str}"}, 500



