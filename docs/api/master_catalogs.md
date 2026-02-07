# API de Catálogos Maestros

Endpoints para recuperar datos de catálogos maestros.

## Alergias

### GET /api/v1/master/allergies/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de alergias.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idalergia": "string",
  "salergia": "string",
  "bactivo": true
}
```


---

## Tipos de Asistencia

### GET /api/v1/master/attendance-types/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de tipos de asistencia.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idtipoasistencia": "string",
  "stipoasistencia": "string",
  "bactivo": true
}
```


---

## Bancos

### GET /api/v1/master/banks/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de bancos.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idbanco": 1,
  "sbanco": "string",
  "bactivo": true
}
```


---

## Tipos de Sangre

### GET /api/v1/master/blood-types/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de tipos de sangre.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idtiposangre": "string",
  "stiposangre": "string",
  "bactivo": true
}
```


---

## Chatbot

### GET /api/v1/master/chatbot/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene datos del chatbot.

**Respuesta**:
Devuelve una lista JSON de objetos.


---

## Ciudades

### GET /api/v1/master/cities/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de ciudades.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idciudad": 1,
  "sciudad": "string",
  "idpais": 1,
  "bactivo": true
}
```


---

## Tipos de Documento

### GET /api/v1/master/document-types/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de tipos de documento.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idtipodocumento": "string",
  "stipodocumento": "string",
  "bactivo": true
}
```


---

## Campos Dinámicos

### GET /api/v1/core/dynamics/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de campos dinámicos.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idcampodinamico": 1,
  "stipoentidad": "string",
  "setiqueta": "string",
  "snombrecampo": "string",
  "stipocampo": "string",
  "brequerido": true,
  "jopciones": {}
}
```


---

## Funcionalidades

### GET /api/v1/master/functionalities/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de funcionalidades.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idfuncionalidad": 1,
  "uuidfuncionalidad": "string",
  "sfuncionalidad": "string",
  "sdescripcion": "string",
  "scodigo": "string",
  "bactivo": true
}
```


---

## Funciones

### GET /api/v1/master/functions/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de funciones.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idfuncion": "string",
  "sfuncion": "string",
  "sdescfuncion": "string",
  "sejemplofuncion": "string",
  "bactivo": true
}
```


---

## Géneros

### GET /api/v1/master/genders/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de géneros.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idsexo": 1,
  "ssexo": "string",
  "bactivo": true
}
```


---

## Instituciones de Seguros de Salud (ARS)

### GET /api/v1/master/health-insurance-institutions/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de instituciones de seguros de salud.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idinstitucionsegmed": "string",
  "sinstitucionsegmed": "string",
  "bactivo": true
}
```


---

## Inteligencia

### GET /api/v1/master/intelligence/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene datos de inteligencia.

**Respuesta**:
Devuelve una lista JSON de objetos.


---

## Estados Civiles

### GET /api/v1/master/marital-status/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de estados civiles.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idestadocivil": 1,
  "sestadocivil": "string",
  "bactivo": true
}
```


---

## Roles Maestros

### GET /api/v1/master/roles/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de roles maestros.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idrol": 1,
  "srol": "string",
  "scodigo": "string",
  "sdescripcion": "string",
  "bactivo": true
}
```


---

## Instituciones Médicas

### GET /api/v1/master/medical-institutions/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de instituciones médicas.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idinstitucionmedica": "string",
  "sinstitucionmedica": "string",
  "bactivo": true
}
```


---

## NCF (Comprobantes Fiscales)

### GET /api/v1/master/ncf/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene datos de NCF.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idsecuencia": 1,
  "stiponcf": "string",
  "sprefijo": "string",
  "inumeroactual": 1,
  "inumeromaximo": 1,
  "bactivo": true,
  "dfechavencimiento": "2024-01-01T12:00:00Z"
}
```


---

## Procesadores de Pago

### GET /api/v1/master/payment-processors/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de procesadores de pago.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idprocesadorpago": 1,
  "sprocesadorpago": "string",
  "bactivo": true
}
```


---

## Tipos de Teléfono

### GET /api/v1/master/phone-types/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de tipos de teléfono.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idtipotelefono": "string",
  "stipotelefono": "string",
  "bactivo": true
}
```


---

## Profesiones

### GET /api/v1/master/professions/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de profesiones.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idprofesion": "string",
  "sprofesion": "string",
  "bactivo": true
}
```


---

## Permisos de Roles

### GET /api/v1/master/role-permissions/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de permisos de roles.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idrolpermiso": 1,
  "idrol": 1,
  "idpantallafuncionalidad": 1,
  "bpermitido": true
}
```


---

## Funcionalidades de Pantalla

### GET /api/v1/master/screen-functionalities/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de funcionalidades de pantalla.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idpantallafuncionalidad": 1,
  "idpantalla": 1,
  "idfuncionalidad": 1,
  "bactivo": true
}
```


---

## Pantallas

### GET /api/v1/master/screens/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de pantallas.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idpantalla": 1,
  "uuidpantalla": "string",
  "idmodulo": 1,
  "spantalla": "string",
  "sdescripcion": "string",
  "sruta": "string",
  "sicono": "string",
  "scodigo": "string",
  "iorden": "string",
  "bactivo": true
}
```


---

## Búsqueda

### GET /api/v1/master/search/

**Requiere Autenticación**: Sí

**Descripción**: Realiza búsquedas globales o específicas.

**Respuesta**:
Devuelve una lista JSON de objetos.


---

## Sectores

### GET /api/v1/master/sectors/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de sectores.

**Respuesta**:
Devuelve una lista JSON de objetos.

### Ejemplo de Respuesta
```json
{
  "idsector": 1,
  "ssector": "string",
  "idciudad": 1,
  "bactivo": true
}
```


---
