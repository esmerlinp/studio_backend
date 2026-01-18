# Student API

## GET /api/v1/students/

Obtiene la lista de todos los estudiantes del esquema actual.

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## GET /api/v1/students/<int:student_id>

Obtiene un estudiante específico por su ID.

**Auth Required**: Yes

### URL Parameters
- `student_id`

### Response
Returns a JSON response.

---

## POST /api/v1/students/

Crea un nuevo estudiante incluyendo campos fijos y dinámicos.

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## PATCH /api/v1/students/<int:student_id>

Actualiza datos de un estudiante (soporta actualización parcial).

**Auth Required**: Yes

### URL Parameters
- `student_id`

### Response
Returns a JSON response.

---

## DELETE /api/v1/students/<int:student_id>

Elimina un estudiante del sistema.

**Auth Required**: Yes

### URL Parameters
- `student_id`

### Response
Returns a JSON response.

---

## PATCH /api/v1/students/<int:student_id>/upload-image

**Auth Required**: Yes

### URL Parameters
- `student_id`

### Response
Returns a JSON response.

---

