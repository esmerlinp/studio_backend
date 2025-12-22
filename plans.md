

# 🧠 Modelo Conceptual – Planes, Precios y Asignación a Clientes

## 🎯 Objetivo del sistema

Permitir:

* Definir **planes comerciales** (qué incluye el producto)
* Definir **listas de precios** (cuánto cuesta y cómo se cobra)
* Asignar **un plan vigente a cada cliente**, manteniendo historial

---

## 🧱 Entidades principales (Dominio)

```
Plan ───< PriceList ───< ClientPlan >─── Client
```

### 1️⃣ Plan (Qué se ofrece)

**Define las capacidades del producto**

Ejemplos:

* BASIC
* STANDARD
* PREMIUM

📌 **No tiene precio**
📌 Cambia poco en el tiempo

---

### 2️⃣ PriceList (Cuánto cuesta)

**Define el precio del plan en un contexto específico**

Ejemplos:

* BASIC – Mensual – USD 20
* BASIC – Anual – USD 200
* PREMIUM – Mensual – USD 50

📌 Pertenece a **un solo Plan**
📌 Puede cambiar con el tiempo (versionado por fechas)
📌 Permite promociones, aumentos, monedas, billing cycles

---

### 3️⃣ ClientPlan (Qué tiene el cliente)

**Une cliente + plan + precio en un periodo de tiempo**

📌 Es el **contrato efectivo**
📌 Guarda historial
📌 Controla vigencia y estado

---

## 🔄 Flujo de Trabajo Conceptual

---

## 🟦 FASE 1 – Creación de Planes (Administración)

### 👤 Actor

Administrador del sistema

### 🔁 Flujo

1. Crear Plan
2. Definir límites y características
3. Activar plan

### 🧠 Reglas

* Un plan puede existir sin precio
* Un plan puede tener múltiples listas de precios

### 📊 Ejemplo

```
Plan:
- code: PREMIUM
- max_users: 100
- support_level: 24/7
```

---

## 🟦 FASE 2 – Creación de Listas de Precios

### 👤 Actor

Administrador / Finanzas

### 🔁 Flujo

1. Seleccionar Plan
2. Crear lista de precio
3. Definir:

   * Ciclo (MONTHLY / ANNUAL)
   * Precio
   * Moneda
   * Validez
4. Activar

### 🧠 Reglas

* Un plan puede tener muchas listas
* Solo una lista activa por:

  ```
  plan + billing_cycle + rango de fechas
  ```
* Nunca se actualiza el precio → se crea una nueva lista

### 📊 Ejemplo

```
PriceList:
- plan: PREMIUM
- billing_cycle: MONTHLY
- price: 50.00
- valid_from: 2025-01-01
```

---

## 🟦 FASE 3 – Asignación de Plan a Cliente

### 👤 Actor

Sistema / Ventas / Onboarding

### 🔁 Flujo

1. Seleccionar cliente
2. Seleccionar plan
3. Seleccionar lista de precios válida
4. Definir fecha de inicio
5. Crear ClientPlan

### 🧠 Reglas críticas

✔ Un cliente **no puede tener dos planes activos al mismo tiempo**
✔ El plan asignado usa **una lista de precios específica**
✔ La relación es temporal (start_date / end_date)

### 📊 Ejemplo

```
ClientPlan:
- client_id: 10
- plan: PREMIUM
- price_list: PREMIUM-MONTHLY-USD
- start_date: 2025-02-01
- status: ACTIVE
```

---

## 🔄 FASE 4 – Cambio de Plan (Upgrade / Downgrade)

### 🔁 Flujo

1. Detectar cambio solicitado
2. Cerrar plan actual:

   * end_date = hoy
   * status = CANCELLED
3. Crear nuevo ClientPlan
4. (Opcional) prorratear

### 🧠 Regla de oro

📌 **Nunca se edita el ClientPlan anterior**
📌 Siempre se crea uno nuevo

---

## 🔄 FASE 5 – Suspensión / Cancelación

### 🔁 Flujo

* Suspensión temporal → `status = SUSPENDED`
* Cancelación → `status = CANCELLED + end_date`

📌 El historial queda intacto

---

## 🧩 Reglas de Dominio Clave (Resumen)

| Regla                        | Descripción                                        |
| ---------------------------- | -------------------------------------------------- |
| Plan ≠ Precio                | El plan define capacidades, el precio define cobro |
| Precio versionado            | Nunca se edita, se reemplaza                       |
| Un plan activo por cliente   | Evita conflictos de facturación                    |
| ClientPlan es histórico      | Auditoría y billing                                |
| PriceList valida pertenencia | Precio debe coincidir con plan                     |

---

## 🧠 Modelo Mental Simplificado

> **Plan** = Qué puede hacer el cliente
> **PriceList** = Cuánto paga
> **ClientPlan** = Contrato activo

---

## 🚀 Evolución Natural del Modelo

Cuando estés listo puedes agregar:

1️⃣ **Invoices**
2️⃣ **Subscriptions**
3️⃣ **Usage-based billing**
4️⃣ **Discounts / Coupons**
5️⃣ **Trials**
6️⃣ **Multi-currency**

---

Si quieres, el próximo paso puede ser:

* 📄 Modelo ER visual
* 🧾 Flujo de facturación
* 💳 Integración con Stripe
* 🧠 Reglas de prorrateo

Tú decides 🔥
