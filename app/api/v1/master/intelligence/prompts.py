REPORT_ESTUDIANTE_TEMPLATE = """
Actúa como un psicopedagogo experto. Analiza los siguientes datos del estudiante en Akdmia, la respuesta debe ser en el idioma ({idioma}) en JSON estructurado:

DATOS:
- Datos Básicos: {datos_basicos}
- Calificaciones: {calificaciones}
- Hábitos Alimenticios: {alimentacion}
- Tareas Recientes: {tareas}
- Notas Adicionales: {notas_adicionales}
- Analisis Anterior: {analisis_anterior}

PROPORCIONA:
1. Resumen del comportamiento general.
2. Relación entre alimentación y rendimiento (si aplica).
3. Tres puntos específicos a mejorar basados en sus tareas y notas.
4. Un mensaje motivacional corto para el estudiante.

PROPORCIONA UN PLAN DE ACCIÓN ESTRUCTURADO (si aplica):

1. IDENTIFICACIÓN DE DEBILIDADES: Analiza qué temas específicos no domina.
2. PARA EL MAESTRO: Sugiere 2 ejercicios técnicos o dinámicas de clase para nivelar al alumno.
3. PARA LOS PADRES: Sugiere 2 actividades cotidianas o ejercicios prácticos para reforzar en casa.
4. RECURSO ESPECÍFICO: Inventa un ejercicio corto de "entrenamiento mental" basado en sus puntos débiles.

"""