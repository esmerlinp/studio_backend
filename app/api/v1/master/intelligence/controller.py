
from app.utils.responses import success, error
from app.services.master_scheme.intelligence_service import generar_reporte_estudiante, ai_generic_generator
from app import limiter, track_activity
from flask_jwt_extended import jwt_required
import json
from app.services.client_scheme.student_service import get_student_by_id

from .prompts import REPORT_ESTUDIANTE_TEMPLATE
from app.utils import i18n

@limiter.limit("10 per minute")
@track_activity
@jwt_required()
def get_report(student_id):
    
    estudiante = get_student_by_id(student_id)
    

    # Simulación de datos extraídos de tu base de datos Akdmia
    #TODO: Reemplazar con datos reales cuando se tengan
    estudiante_ejemplo = {
        "idioma":i18n.get_locale(),
        "datos_basicos": {
            "nombre": estudiante.firstName + " " + estudiante.lastName,
            "edad":"14 años",
            "grado": "Octavo"
        },
        "calificaciones": {"Matemáticas": 55, 
                           "Lenguaje": 90, 
                           "Ciencias": 78, 
                           "Historia": 88},
        "alimentacion": [{"fecha": "2024-09-01", "comida": "Desayuno: Cereal, Almuerzo: Pollo con arroz, Cena: Pasta"},
                  {"fecha": "2024-09-02", "comida": "Desayuno: Panqueques, Almuerzo: Ensalada, Cena: Pescado con vegetales"}],
        "tareas": [{"asignatura": "Matemáticas", "tarea": "Resolver problemas de álgebra", "fecha_entrega": "2024-09-05"},
                  {"asignatura": "Ciencias", "tarea": "Investigar sobre el sistema solar", "fecha_entrega": "2024-09-07"}],
        "notas_adicionales": "Entregó tarde el proyecto de Geometría. Excelente redacción en el ensayo de Lenguaje.",
        "analisis_anterior": {}
    }

    #return success(data=estudiante_ejemplo)
    # Ejecución
    reporte = ai_generic_generator(REPORT_ESTUDIANTE_TEMPLATE, estudiante_ejemplo)
    data_json = json.loads(reporte.replace("```json", "").replace("```", ""))

    return success(data=data_json)