from enum import Enum


class ResourceTypes:
    # --- CORE SISTEMA & AUTH ---
    USER = "usuarios"
    USER_SESSION = "usuariossesiones"
    USER_CLIENT = "usuariosclientes"
    USER_PREFERENCE = "usuariospreferencias"
    USER_ROLE = "usuariosroles"
    ROLE = "roles"
    ROLE_PERMISSION = "rolespermisos"
    
    # --- FACTURACIÓN & PLANES (STRIPE / DGII) ---
    CLIENT = "clientes"
    CLIENT_PLAN = "planesclientes"
    PLAN = "planes"
    PRICE_LIST = "listasprecios"
    INVOICE = "facturas"
    PAYMENT_TRANSACTION = "transacciones_pagos"
    NCF = "ncf"
    NCF_LOG = "ncflog"
    WEBHOOK_LOG = "logs_webhooks"
    CURRENCY = "monedas"
    
    # --- ESTRUCTURA APLICACIÓN ---
    MODULE = "modulos"
    FUNCTIONALITY = "funcionalidades"
    FUNCTION = "funciones"
    SCREEN = "pantallas"
    SCREEN_FUNCTIONALITY = "pantallasfuncionalidades"
    STORAGE = "cuotasalmacenamiento"
    
    # --- UBICACIÓN GEOGRÁFICA ---
    COUNTRY = "paises"
    CITY = "ciudades"
    SECTOR = "sectores"
    
    # --- DATOS MAESTROS ACADÉMICOS & SALUD ---
    ALLERGY = "alergias"
    BLOOD_TYPE = "tipossangre"
    MEDICAL_INSTITUTION = "institucionesmedicas"
    INSURANCE_INSTITUTION = "institucionessegmed"
    CIVIL_STATUS = "estadosciviles"
    GENDER = "sexos"
    PROFESSION = "profesiones"
    OTHER_COLLEGE = "otroscolegios"
    DOCUMENT_TYPE = "tiposdocumento"
    PHONE_TYPE = "tipostelefono"
    ATTENDANCE_TYPE = "tiposasistencia"

    # --- ESQUEMA CLIENTE (AUDIT) ---
    AUDIT = "auditoria"
    STUDENT = "estudiantes"
    GRADE = "grados"
    
    
class ActionType(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    MARK_AS_DELETE = "MARK_AS_DELETE"
    READ = "READ"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    DOWNLOAD = "DOWNLOAD"
    UPLOAD = "UPLOAD"
    PRINT = "PRINT"
    ERROR = "ERROR"