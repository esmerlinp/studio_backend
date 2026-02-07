# API de Roles

## GET /api/v1/core/roles/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de roles.

**Respuesta**:
Devuelve una respuesta JSON con la lista de roles.

### Ejemplo de Respuesta
```json
[
  {
    "idrol": 1,
    "srol": "string",
    "scodigo": "string",
    "sdescripcion": "string",
    "bactivo": true
  }
]
```


---

## POST /api/v1/core/roles/

**Requiere Autenticación**: Sí

**Descripción**: Crea un nuevo rol.

**Parámetros del Cuerpo**:
- `description`: Descripción del rol.
- `code`: Código del rol.
- `name`: Nombre del rol.

**Respuesta**:
Devuelve una respuesta JSON con el rol creado.

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

## DELETE /api/v1/core/roles/<int:role_id>

**Requiere Autenticación**: Sí

**Descripción**: Elimina un rol existente.

**Parámetros de URL**:
- `role_id`: ID del rol a eliminar.

**Respuesta**:
Devuelve una respuesta JSON confirmando la eliminación.

---
