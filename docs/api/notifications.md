# Notifications API

## GET /api/v1/user/notifications/

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## PUT /api/v1/user/notifications/mark_read

**Auth Required**: Yes

### Body Parameters
- `notif_id`

### Response
Returns a JSON response.

---

## POST /api/v1/user/notifications/

**Auth Required**: Yes

### Body Parameters
- `title`
- `resource_id`
- `resource_type`
- `message`
- `target_url`

### Response
Returns a JSON response.

---

