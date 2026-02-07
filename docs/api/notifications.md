# API de Notificaciones

## GET /api/v1/user/notifications/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de notificaciones del usuario.

**Respuesta**:
Devuelve una respuesta JSON.

### Ejemplo de Respuesta
```json
[
  {
    "idnotificacion": 1,
    "idusuario": 1,
    "stitulo": "string",
    "smensaje": "string",
    "stiporecurso": "string",
    "idrecurso": 1,
    "saccion": "string",
    "surltarget": "string",
    "bleida": true,
    "dfechacreacion": "2024-01-01T12:00:00Z"
  }
]
```


---

## PUT /api/v1/user/notifications/mark_read

**Requiere Autenticación**: Sí

**Descripción**: Marca una notificación como leída.

**Parámetros del Cuerpo**:
- `notif_id`: ID de la notificación.

**Respuesta**:
Devuelve una respuesta JSON.

---

## POST /api/v1/user/notifications/

**Requiere Autenticación**: Sí

**Descripción**: Crea una nueva notificación.

**Parámetros del Cuerpo**:
- `title`: Título de la notificación.
- `resource_id`: ID del recurso relacionado.
- `resource_type`: Tipo de recurso.
- `message`: Mensaje de la notificación.
- `target_url`: URL de destino.

**Respuesta**:
Devuelve una respuesta JSON.

### Ejemplo de Respuesta
```json
{
  "idnotificacion": 1,
  "idusuario": 1,
  "stitulo": "string",
  "smensaje": "string",
  "stiporecurso": "string",
  "idrecurso": 1,
  "saccion": "string",
  "surltarget": "string",
  "bleida": true,
  "dfechacreacion": "2024-01-01T12:00:00Z"
}
```


---
