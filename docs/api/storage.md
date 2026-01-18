# Storage API

## GET /api/v1/documents/

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## POST /api/v1/documents/upload

**Auth Required**: Yes

### Body Parameters
- `entity_name`
- `file_name`
- `entity_record`

### Response
Returns a JSON response.

---

## GET /api/v1/documents/<int:document_id>

**Auth Required**: Yes

### URL Parameters
- `document_id`

### Response
Returns a JSON response.

---

## DELETE /api/v1/documents/<int:document_id>

**Auth Required**: Yes

### URL Parameters
- `document_id`

### Response
Returns a JSON response.

---

