# Descripción del Proyecto: Studio Backend

Este proyecto es el backend para una plataforma de gestión (Studio), desarrollado con **Flask** (Python). Utiliza una arquitectura multi-inquilino (multi-tenant) basada en esquemas de base de datos PostgreSQL.

## Tecnologías Principales
- **Framework:** Flask (Python)
- **Base de Datos:** PostgreSQL (con SQLAlchemy)
- **Autenticación:** JWT (Flask-JWT-Extended)
- **Pagos:** Stripe API
- **Infraestructura:** Docker, Google Cloud (GCS para almacenamiento)
- **Internacionalización (i18n):** Soporte multi-idioma (es, en)

## Arquitectura Multi-tenant
El sistema utiliza un modelo de **esquemas aislados** en PostgreSQL:
- **Esquema `public` (o `master`):** Contiene información global como usuarios, clientes, planes de suscripción y países.
- **Esquemas de Clientes:** Cada cliente (empresa) tiene su propio esquema donde se almacenan sus datos específicos (estudiantes, roles locales, documentos, etc.). La aplicación cambia el `search_path` dinámicamente según el usuario autenticado.

## Estructura de Directorios

```text
studio_backend/
├── app/                    # Directorio principal de la aplicación
│   ├── api/                # Definición de rutas y controladores API
│   │   └── v1/
│   │       ├── base/       # Funcionalidades específicas del cliente (estudiantes, roles)
│   │       └── master/     # Funcionalidades globales (auth, clientes, planes, pagos)
│   ├── models/             # Modelos de SQLAlchemy (master_scheme y client_scheme)
│   ├── services/           # Lógica de negocio separada de las rutas
│   ├── utils/              # Funciones auxiliares (i18n, helpers de red, respuestas)
│   ├── extensions.py       # Inicialización de extensiones (DB, JWT, etc.)
│   └── templates/          # Plantillas HTML para correos y vistas simples
├── docs/                   # Documentación técnica
├── run.py                  # Punto de entrada y configuración de middleware
├── requirements.txt        # Dependencias de Python
└── Dockerfile              # Configuración para despliegue en contenedores
```

## Funcionalidades Actuales

### 1. Gestión de Autenticación y Usuarios
- Registro y login con JWT.
- Recuperación de contraseña mediante tokens por correo.
- Gestión de preferencias de usuario (idioma, zona horaria, formatos de fecha).
- Confirmación de cuenta.

### 2. Sistema de Suscripciones y Pagos (Master)
- Integración completa con **Stripe**.
- Manejo de planes de suscripción.
- Pasarela de facturación y webhook para eventos de pago.
- Flujo de "onboarding" para nuevos clientes.

### 3. Gestión de Clientes (Multi-tenancy)
- Creación dinámica de esquemas de base de datos.
- Aislamiento de datos por cliente.
- Middleware en `run.py` que asegura el contexto correcto de base de datos por petición.

### 4. Funcionalidades de Negocio (Base)
- **Estudiantes:** Gestión de perfiles de estudiantes.
- **Documentos:** Sistema de almacenamiento (posiblemente vinculado a GCS).
- **Roles y Permisos:** Control de acceso basado en roles tanto a nivel global como local por cliente.
- **Campos Dinámicos:** Soporte para campos personalizados.

### 5. Utilidades y Sistema
- Soporte internacional (i18n) para respuestas de error y plantillas.
- Registro de auditoría (logs) para administradores.
- Sistema de notificaciones.
- Inteligencia (análisis de datos o reportes básicos).

---
*Este documento fue generado automáticamente como parte del análisis de estructura y funcionalidad del proyecto.*
