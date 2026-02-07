# API de Vistas del Esquema de Cliente

Estos endpoints proporcionan acceso de solo lectura a varias vistas de datos específicas del cliente.

## Asistencias de Ciclo Activo

### GET /api/v1/client/active-cycle-attendances/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de asistencias del ciclo activo.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idasistencia": 1,
  "dfecha": "2024-01-01T12:00:00Z",
  "scomentario": "string",
  "idtipoasistencia": 1,
  "stipoasistencia": "string",
  "idestudiante": 1,
  "scodigoestudiante": "string",
  "sestudiante": "string",
  "dfechanacimiento": "2024-01-01T12:00:00Z",
  "iedad": 1,
  "idsexo": 1,
  "ssexo": "string",
  "idciclo": 1,
  "sciclo": "string",
  "idnivel": 1,
  "snivel": "string",
  "idcurso": 1,
  "idaula": 1,
  "scursoaula": "string",
  "idestudianteaulacic": 1
}
```


---

## Competencias de Ciclo Activo

### GET /api/v1/client/active-cycle-competencies/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de competencias del ciclo activo.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idsubciccompetenciacurso": 1,
  "idsubciclo": 1,
  "ssubciclo": "string",
  "iordensubcic": 1,
  "idcompetencia": 1,
  "scompetencia": "string",
  "idcurso": 1,
  "scurso": "string",
  "idnivel": 1,
  "snivel": "string",
  "iperiodos": 1,
  "bpermiterecuperacion": true
}
```


---

## Cursos de Ciclo Activo

### GET /api/v1/client/active-cycle-courses/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de cursos del ciclo activo.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idciclo": 1,
  "idsubciclo": 1,
  "idcurso": 1,
  "idasignatura": 1,
  "sciclo": "string",
  "ssubciclo": "string",
  "iordensubcic": 1,
  "scurso": "string",
  "iordencurso": 1,
  "sasignatura": "string",
  "idareatematica": 1,
  "sareatematica": "string",
  "iordenasignatura": 1,
  "icreditosasignatura": 1
}
```


---

## Correcciones de Notas de Ciclo Activo

### GET /api/v1/client/active-cycle-grade-corrections/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de correcciones de notas del ciclo activo.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idnotacorreccion": 1,
  "dfechasolicitud": "string",
  "dfechaprocesada": "string",
  "idestudiante": 1,
  "snombreresponsable": "string",
  "idnivel": 1,
  "snivel": "string",
  "idcurso": 1,
  "scurso": "string",
  "idciclo": 1,
  "sciclo": "string",
  "idasignatura": 1,
  "sasignatura": "string",
  "idprofesor": 1,
  "sprofesor": "string",
  "idparcial": 1,
  "sparcial": "string",
  "idcompetencia": 1,
  "scompetencia": "string",
  "nnotaant": 0.0,
  "nnotanueva": 0.0,
  "sestado": "string",
  "smotivo": "string",
  "scomentario": "string"
}
```


---

## Notas de Estudiantes de Ciclo Activo

### GET /api/v1/client/active-cycle-student-grades/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de notas de estudiantes del ciclo activo.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idregistro": 1,
  "idestudiante": 1,
  "snombreresponsable": "string",
  "idcurso": 1,
  "scurso": "string",
  "idciclo": 1,
  "idasignatura": 1,
  "sasignatura": "string",
  "idparcial": 1,
  "sparcial": "string",
  "idcompetencia": 1,
  "scompetencia": "string",
  "nnota": 0.0,
  "sliteral": "string"
}
```


---

## Estudiantes de Ciclo Activo

### GET /api/v1/client/active-cycle-students/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de estudiantes del ciclo activo.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idestudianteaulacic": 1,
  "idestudiante": 1,
  "idciclo": 1,
  "idaula": 1,
  "idcurso": 1,
  "scodigoestudiante": "string",
  "sestudiante": "string",
  "scursoaula": "string",
  "idsexo": 1,
  "sciclo": "string",
  "scurso": "string",
  "saula": "string",
  "iestadoestudiante": 1,
  "idnivel": 1
}
```


---

## Asistencias

### GET /api/v1/client/attendances/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de asistencias.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idasistencia": 1,
  "dfecha": "2024-01-01T12:00:00Z",
  "scomentario": "string",
  "idtipoasistencia": 1,
  "stipoasistencia": "string",
  "idestudiante": 1,
  "scodigoestudiante": "string",
  "sestudiante": "string",
  "idestudianteaulacic": 1,
  "dfechanacimiento": "2024-01-01T12:00:00Z",
  "iedad": 1,
  "idsexo": 1,
  "ssexo": "string",
  "idciclo": 1,
  "sciclo": "string",
  "idnivel": 1,
  "snivel": "string",
  "idcurso": 1,
  "idaula": 1,
  "scursoaula": "string"
}
```


---

## Descuentos por Hijos

### GET /api/v1/client/child-discounts/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de descuentos por hijos.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "inumhijo": 1,
  "idciclo": 1,
  "ivalor": 0.0,
  "stipodescuento": "string",
  "stipodescuentodescripcion": "string"
}
```


---

## Lista de Competencias

### GET /api/v1/client/competencies-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de competencias.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idcompetencia": 1,
  "scompetencia": "string",
  "sdescripcion": "string",
  "iorden": 1,
  "bactivo": true
}
```


---

## Lista de Conceptos

### GET /api/v1/client/concepts-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de conceptos.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idconcepto": 1,
  "sconcepto": "string",
  "bfamiliar": true,
  "brecurrente": true,
  "bactivo": true,
  "baplicadescuento": true,
  "baplicarecargo": true,
  "baplicaitbis": true
}
```


---

## Lista de Cursos

### GET /api/v1/client/courses-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de cursos.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idcurso": 1,
  "scurso": "string",
  "idnivel": 1,
  "snivel": "string",
  "iedadpromedio": 1,
  "idcursosiguiente": 1,
  "scursosiguiente": "string",
  "iorden": 1,
  "bactivo": true
}
```


---

## Impuestos Actuales

### GET /api/v1/client/current-taxes/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de impuestos actuales.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idimpuesto": 1,
  "dfecha": "2024-01-01T12:00:00Z",
  "nporciento": 0.0,
  "bactivo": true
}
```


---

## Bloques Horarios por Nivel de Ciclo

### GET /api/v1/client/cycle-level-schedule-blocks/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de bloques horarios por nivel de ciclo.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idciclonivbloqhor": 1,
  "idciclo": 1,
  "sciclo": "string",
  "idnivel": 1,
  "snivel": "string",
  "idbloquehorario": 1,
  "sbloquehorario": "string"
}
```


---

## Lista de Parciales de Ciclo

### GET /api/v1/client/cycle-partials-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de parciales de ciclo.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idsubcicparcial": 1,
  "idsubciclo": 1,
  "ssubciclo": "string",
  "idciclo": 1,
  "sciclo": "string",
  "idparcial": 1,
  "sparcial": "string",
  "sparcialcorto": "string",
  "idnivel": 1,
  "snivel": "string",
  "nminimo": 0.0,
  "nmaximo": 0.0,
  "nminimoaprueba": 0.0,
  "bformula": true,
  "idformula": 1,
  "sformula": "string"
}
```


---

## Ciclos

### GET /api/v1/client/cycles/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de ciclos.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idciclo": 1,
  "sciclo": "string",
  "dfechainicio": "2024-01-01T12:00:00Z",
  "dfechafin": "2024-01-01T12:00:00Z",
  "bactivo": true,
  "ncantsubciclos": 1,
  "ncantestudiantes": 1
}
```


---

## Solicitudes de Evaluación

### GET /api/v1/client/evaluation-requests/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de solicitudes de evaluación.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idsolicitud": 1,
  "idcurso": 1,
  "scurso": "string",
  "idsexo": 1,
  "ssexo": "string",
  "idempevaluador": 1,
  "sestudiante": "string",
  "dfechanacimiento": "string",
  "sdecision": "string",
  "sevaluador": "string",
  "dfechaevaluacion": "string",
  "iestadoevaluacion": 1,
  "binscrito": true,
  "idciclo": 1,
  "sciclo": "string"
}
```


---

## Lista de Fórmulas

### GET /api/v1/client/formulas-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de fórmulas.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idformula": 1,
  "sdescformula": "string",
  "sformula": "string",
  "bactivo": true
}
```


---

## Lista de Correcciones de Notas

### GET /api/v1/client/grade-corrections-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de correcciones de notas.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idnotacorreccion": 1,
  "idnota": 1,
  "idciclo": 1,
  "sciclo": "string",
  "idsubciclo": 1,
  "ssubciclo": "string",
  "idcurso": 1,
  "scurso": "string",
  "idaula": 1,
  "saula": "string",
  "scursoaula": "string",
  "idestudiante": 1,
  "scodigoestudiante": "string",
  "sestudiante": "string",
  "idasignatura": 1,
  "sasignatura": "string",
  "idareatematica": 1,
  "sareatematica": "string",
  "idparcial": 1,
  "sparcial": "string",
  "sparcialcorto": "string",
  "inotaant": 0.0,
  "inotaact": 0.0,
  "scomentario": "string",
  "dfechacambio": "string",
  "idestudianteaulacic": 1
}
```


---

## Lista de Inscripciones

### GET /api/v1/client/inscriptions-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de inscripciones.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idsolicitud": 1,
  "idciclo": 1,
  "sciclo": "string",
  "sestudiante": "string",
  "dfechanacimiento": "string",
  "ssexo": "string",
  "idcurso": 1,
  "scurso": "string"
}
```


---

## Lista de Niveles

### GET /api/v1/client/levels-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de niveles.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idnivel": 1,
  "snivel": "string",
  "bactivo": true
}
```


---

## Lista de Parciales

### GET /api/v1/client/partials-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de parciales.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idparcial": 1,
  "sparcial": "string",
  "sparcialcorto": "string",
  "bactivo": true,
  "bformula": true,
  "idformula": 1
}
```


---

## Calendario de Pagos

### GET /api/v1/client/payment-calendar/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el calendario de pagos.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idcalendariopago": 1,
  "idciclo": 1,
  "sciclo": "string",
  "idfrecuenciapago": 1,
  "sfrecuenciapago": "string",
  "inumerocuota": 1,
  "snombremes": "string",
  "dfechapago": "2024-01-01T12:00:00Z",
  "dfechadescpp": "2024-01-01T12:00:00Z",
  "dfecharec": "2024-01-01T12:00:00Z",
  "bciclo_activo": true,
  "icantpagos": 1
}
```


---

## Frecuencias de Pago

### GET /api/v1/client/payment-frequencies-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de frecuencias de pago.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idfrecuenciapago": 1,
  "sfrecuenciapago": "string",
  "icantpagos": 1,
  "bactivo": true
}
```


---

## Lista de Solicitudes

### GET /api/v1/client/requests-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de solicitudes.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idsolicitud": 1,
  "ssolicitante": "string",
  "idcurso": 1,
  "scurso": "string",
  "snombreresponsable": "string",
  "stelefonoresponsable": "string",
  "iestadoevaluacion": 1,
  "binscrito": true,
  "sestadoprocesosolicitud": "string"
}
```


---

## Detalles de Bloques Horarios

### GET /api/v1/client/schedule-block-details/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de detalles de bloques horarios.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idbloquehorario": 1,
  "inumerofila": 1,
  "sbloquehorario": "string",
  "bactivo": true,
  "thorainicio": "string",
  "thorafin": "string",
  "blunes": true,
  "bmartes": true,
  "bmiercoles": true,
  "bjueves": true,
  "bviernes": true,
  "bsabado": true,
  "bdomingo": true
}
```


---

## Bloques Horarios

### GET /api/v1/client/schedule-blocks/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de bloques horarios.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idbloquehorario": 1,
  "sbloquehorario": "string",
  "bactivo": true,
  "itotalbloquesactivos": 1
}
```


---

## Pagos Escolares

### GET /api/v1/client/school-payments/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de pagos escolares.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idpago": 1,
  "dfechapago": "string",
  "nmonto": 0.0,
  "idestudiante": 1,
  "snombreresponsable": "string",
  "idciclo": 1,
  "sciclo": "string",
  "idconcepto": 1,
  "sconcepto": "string",
  "sfpago": "string",
  "scomentario": "string"
}
```


---

## Balances de Cargos de Estudiantes

### GET /api/v1/client/student-charge-balances/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de balances de cargos de estudiantes.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idestudiantecargocic": 1,
  "idestudiante": 1,
  "scodigoestudiante": "string",
  "sestudiante": "string",
  "dfechanacimiento": "2024-01-01T12:00:00Z",
  "iedad": 1,
  "idsexo": 1,
  "ssexo": "string",
  "idestudiantefam": 1,
  "scodfam": "string",
  "idciclo": 1,
  "sciclo": "string",
  "idnivel": 1,
  "snivel": "string",
  "idcurso": 1,
  "idaula": 1,
  "scursoaula": "string",
  "idestudianteaulacic": 1,
  "idconcepto": 1,
  "sconcepto": "string",
  "bfamiliar": true,
  "brecurrente": true,
  "icuota": 1,
  "nmontocargo": 0.0,
  "ntotal_recargos": 0.0,
  "ntotal_descuentos": 0.0,
  "ntotal_itbis": 0.0,
  "ntotal_pagado": 0.0,
  "nbalance": 0.0,
  "iresponsable": 1,
  "stiporesponsable": "string",
  "snombreresponsable": "string",
  "stelefonoresponsable": "string",
  "scorreoresponsable": "string"
}
```


---

## Lista de Estudiantes

### GET /api/v1/client/students-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de estudiantes.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idestudiante": 1,
  "scodigoestudiante": "string",
  "sestudiante": "string",
  "dfechanacimiento": "string",
  "iedad": 1,
  "dfechainscripcion": "string",
  "idnivel": 1,
  "snivel": "string",
  "idcurso": 1,
  "idaula": 1,
  "scursoaula": "string",
  "idciclo": 1,
  "sciclo": "string",
  "iresponsable": 1,
  "snombreresponsable": "string",
  "stelefonoresponsable": "string",
  "scorreoresponsable": "string",
  "scodfam": "string",
  "iestadoestudiante": 1,
  "sestadoestudiante": "string",
  "idsexo": 1,
  "ssexo": "string",
  "ivive": 1,
  "svive": "string",
  "idpais": 1,
  "spais": "string",
  "idciudad": 1,
  "sciudad": "string",
  "idsector": 1,
  "ssector": "string",
  "sdireccion": "string",
  "idcolegioprocedencia": 1,
  "scolegioprocedencia": "string",
  "idtiposangre": 1,
  "stiposangre": "string",
  "snombremedico": "string",
  "stelefonomedico": "string",
  "snumeroseguromedico": "string",
  "idinstitucionmedica": 1,
  "sinstitucionmedica": "string",
  "idinstitucionsegmed": 1,
  "sinstitucionsegmed": "string",
  "idsolicitud": 1,
  "idestudiantefam": 1,
  "idestudianteaulacic": 1
}
```


---

## Competencias de Curso por Subciclo

### GET /api/v1/client/sub-cycle-course-competencies/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de competencias de curso por subciclo.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idsubciccompetenciacurso": 1,
  "idsubciclo": 1,
  "ssubciclo": "string",
  "idcurso": 1,
  "scurso": "string",
  "idcompetencia": 1,
  "scompetencia": "string",
  "scompetenciadescripcion": "string",
  "idciclo": 1,
  "idasignatura": 1,
  "sasignatura": "string"
}
```


---

## Lista de Subciclos

### GET /api/v1/client/sub-cycles-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de subciclos.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idsubciclo": 1,
  "ssubciclo": "string",
  "iordensubcic": 1,
  "idciclo": 1,
  "sciclo": "string",
  "bactivo": true
}
```


---

## Áreas Temáticas

### GET /api/v1/client/subject-areas/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de áreas temáticas.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idareatematica": 1,
  "sareatematica": "string",
  "bactivo": true
}
```


---

## Asignaturas

### GET /api/v1/client/subjects/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de asignaturas.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idasignatura": 1,
  "sasignatura": "string",
  "idareatematica": 1,
  "sareatematica": "string",
  "iorden": 1,
  "icreditos": 1,
  "bactivo": true
}
```


---

## Recargos por Día

### GET /api/v1/client/surcharges-per-day-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de recargos por día.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idrecxdia": 1,
  "idciclo": 1,
  "idias": 1,
  "nvalor": 0.0,
  "stipo": "string",
  "stipodescripcion": "string"
}
```


---

## Lista de Impuestos

### GET /api/v1/client/taxes-list/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de impuestos.

**Parámetros de Consulta**:
- `page` (opcional): Número de página para paginación.
- `per_page` (opcional): Elementos por página.
- `filters` (opcional): Varios campos disponibles en la vista para filtrar.

**Respuesta**:
Devuelve un objeto JSON que contiene la lista y los metadatos de paginación.

### Ejemplo de Respuesta
```json
{
  "idimpuesto": 1,
  "dfecha": "string",
  "nporciento": 0.0,
  "bactivo": true
}
```


---
