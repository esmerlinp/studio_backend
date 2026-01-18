# Clients API

## GET /api/v1/clients/

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## GET /api/v1/clients/<int:clientId>

**Auth Required**: Yes

### URL Parameters
- `clientId`

### Response
Returns a JSON response.

---

## GET /api/v1/clients/<int:clientId>/plan

**Auth Required**: Yes

### URL Parameters
- `clientId`

### Response
Returns a JSON response.

---

## GET /api/v1/clients/<int:clientId>/plan/all

**Auth Required**: Yes

### URL Parameters
- `clientId`

### Response
Returns a JSON response.

---

## GET /api/v1/clients/<int:clientId>/payments/orders

**Auth Required**: Yes

### URL Parameters
- `clientId`

### Response
Returns a JSON response.

---

## GET /api/v1/clients/settings

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## GET /api/v1/clients/logs

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## PATCH /api/v1/clients/plan/change

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## POST /api/v1/clients/

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## POST /api/v1/clients/onboard

**Auth Required**: No

### Body Parameters
- `user_data`
- `client_data`
- `plan_data`

### Response
Returns a JSON response.

---

## POST /api/v1/clients/export-data

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## POST /api/v1/clients/request-deletion

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## POST /api/v1/clients/cancel-deletion

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## POST /api/v1/clients/cleanup

**Auth Required**: Yes

### Response
Returns a JSON response.

---

