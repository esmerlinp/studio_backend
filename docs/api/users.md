# API de Usuarios

## GET /api/v1/user/

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el listado de usuarios.

**Respuesta**:
Devuelve una lista de usuarios.

### Ejemplo de Respuesta
```json
{}
```

---

## GET /api/v1/user/<userId>

**Requiere Autenticación**: Sí

**Parámetros de URL**:
- `userId`: ID del usuario.

**Respuesta**:
Devuelve los detalles del usuario.

### Ejemplo de Respuesta
```json
{}
```

---

## PUT /api/v1/user/<userId>/desactivate

**Requiere Autenticación**: Sí

**Parámetros de URL**:
- `userId`: ID del usuario a desactivar.

**Respuesta**:
Devuelve el usuario desactivado.

### Ejemplo de Respuesta
```json
{}
```

---

## GET /api/v1/user/<userName>

**Requiere Autenticación**: Sí

**Parámetros de URL**:
- `userName`: Nombre de usuario.

**Respuesta**:
Devuelve los detalles del usuario.

### Ejemplo de Respuesta
```json
{}
```

---

## GET /api/v1/user/me

**Requiere Autenticación**: Sí

**Descripción**: Obtiene la información del usuario actual autenticado.

**Respuesta**:
Devuelve los datos del usuario.

### Ejemplo de Respuesta
```json
{}
```

---

## GET /api/v1/user/organization

**Requiere Autenticación**: Sí

**Descripción**: Obtiene la organización del usuario actual.

**Respuesta**:
Devuelve los datos de la organización (Cliente).

### Ejemplo de Respuesta
```json
{}
```

---

## GET /api/v1/user/subscription

**Requiere Autenticación**: Sí

**Descripción**: Obtiene la suscripción del usuario actual.

**Respuesta**:
Devuelve los datos de la suscripción.

### Ejemplo de Respuesta
```json
{}
```

---

## GET /api/v1/user/payments

**Requiere Autenticación**: Sí

**Descripción**: Obtiene los pagos del usuario actual.

**Respuesta**:
Devuelve el historial de pagos.

### Ejemplo de Respuesta
```json
{}
```

---

## GET /api/v1/user/sessions

**Requiere Autenticación**: Sí

**Descripción**: Obtiene las sesiones activas del usuario.

**Respuesta**:
Devuelve la lista de sesiones.

### Ejemplo de Respuesta
```json
{}
```

---

## GET /api/v1/user/storage

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el uso de almacenamiento.

**Respuesta**:
Devuelve los datos de almacenamiento.

### Ejemplo de Respuesta
```json
{}
```

---

## GET /api/v1/user/audit

**Requiere Autenticación**: Sí

**Descripción**: Obtiene los registros de auditoría.

**Respuesta**:
Devuelve la lista de logs.

### Ejemplo de Respuesta
```json
{}
```

---

## GET /api/v1/user/audit/<string:entityName>

**Requiere Autenticación**: Sí

**Descripción**: Obtiene los registros de auditoría para una entidad específica.

**Respuesta**:
Devuelve la lista de logs filtrada.

### Ejemplo de Respuesta
```json
{}
```

---

## GET /api/v1/user/notifications

**Requiere Autenticación**: Sí

**Descripción**: Obtiene las notificaciones.

**Respuesta**:
Devuelve la lista de notificaciones.

### Ejemplo de Respuesta
```json
{}
```

---

## GET /api/v1/user/plan

**Requiere Autenticación**: Sí

**Descripción**: Obtiene el plan activo.

**Respuesta**:
Devuelve los datos del plan.

### Ejemplo de Respuesta
```json
{}
```

---

## POST /api/v1/user/

**Requiere Autenticación**: Sí (Admin)

**Parámetros del Cuerpo**:
- `userName`: Nombre de usuario.
- `lastName`: Apellido.
- `firstName`: Nombre.
- `email`: Correo electrónico.

**Respuesta**:
Devuelve el usuario creado.

### Ejemplo de Respuesta
```json
{}
```

---

## POST /api/v1/user/changepassword

**Requiere Autenticación**: Sí

**Parámetros del Cuerpo**:
- `new_password`: Nueva contraseña.
- `sessionId`: ID de sesión.

**Respuesta**:
Devuelve el usuario actualizado o mensaje de éxito.

### Ejemplo de Respuesta
```json
{}
```

---

## POST /api/v1/user/forgot-password

**Requiere Autenticación**: No

**Parámetros del Cuerpo**:
- `email`: Correo electrónico.

**Respuesta**:
Mensaje de confirmación.

### Ejemplo de Respuesta
```json
{}
```

---

## POST /api/v1/user/preferences/default

**Requiere Autenticación**: Sí

**Respuesta**:
Devuelve las preferencias por defecto.

### Ejemplo de Respuesta
```json
{}
```

---

## PUT /api/v1/user/preferences

**Requiere Autenticación**: Sí

**Respuesta**:
Devuelve las preferencias actualizadas.

### Ejemplo de Respuesta
```json
{}
```

---
