# Users API

## GET /api/v1/users/

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## GET /api/v1/users/<userId>

**Auth Required**: Yes

### URL Parameters
- `userId`

### Response
Returns a JSON response.

---

## PUT /api/v1/users/<userId>/desactivate

**Auth Required**: Yes

### URL Parameters
- `userId`

### Response
Returns a JSON response.

---

## GET /api/v1/users/<userName>

**Auth Required**: Yes

### URL Parameters
- `userName`

### Response
Returns a JSON response.

---

## GET /api/v1/users/current

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## GET /api/v1/users/current/organization

**Auth Required**: No

### Response
Returns a JSON response.

---

## GET /api/v1/users/current/subscription

**Auth Required**: No

### Response
Returns a JSON response.

---

## GET /api/v1/users/current/payments

**Auth Required**: No

### Response
Returns a JSON response.

---

## GET /api/v1/users/current/sessions

**Auth Required**: No

### Response
Returns a JSON response.

---

## GET /api/v1/users/current/storage

**Auth Required**: No

### Response
Returns a JSON response.

---

## GET /api/v1/users/current/audit

**Auth Required**: No

### Response
Returns a JSON response.

---

## GET /api/v1/users/current/audit/<string:entityName>

**Auth Required**: No

### Response
Returns a JSON response.

---

## GET /api/v1/users/current/notifications

**Auth Required**: No

### Response
Returns a JSON response.

---

## GET /api/v1/users/current/plan

**Auth Required**: No

### Response
Returns a JSON response.

---

## POST /api/v1/users/

**Auth Required**: No

### Body Parameters
- `userName`
- `lastName`
- `firstName`
- `email`

### Response
Returns a JSON response.

---

## POST /api/v1/users/changepassword

**Auth Required**: Yes

### Body Parameters
- `new_password`
- `sessionId`

### Response
Returns a JSON response.

---

## POST /api/v1/users/forgot-password

**Auth Required**: No

### Body Parameters
- `email`

### Response
Returns a JSON response.

---

## POST /api/v1/users/preferences/default

**Auth Required**: Yes

### Response
Returns a JSON response.

---

## PUT /api/v1/users/current/preferences

**Auth Required**: Yes

### Response
Returns a JSON response.

---

