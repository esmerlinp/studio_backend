# Plan API

## GET /api/v1/plans/

**Auth Required**: No

### Response
Returns a JSON response.

---

## GET /api/v1/plans/prices-list

**Auth Required**: Yes

### URL Parameters
- `plan_id`

### Response
Returns a JSON response.

---

## GET /api/v1/plans/prices-list/<int:plan_id>

**Auth Required**: Yes

### URL Parameters
- `plan_id`

### Response
Returns a JSON response.

---

## POST /api/v1/plans/

**Auth Required**: Yes

### Body Parameters
- `description`
- `max_users`
- `environment_type`
- `name`
- `max_storage_gb`
- `code`
- `suppor_level`

### Response
Returns a JSON response.

---

## POST /api/v1/plans/prices-list

**Auth Required**: Yes

### Body Parameters
- `min_users`
- `price_per_user`
- `valid_to`
- `features_config`
- `price`
- `billing_cycle`
- `currency`
- `plan_id`
- `valid_from`

### Response
Returns a JSON response.

---

