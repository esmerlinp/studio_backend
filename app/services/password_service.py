import re
from typing import Tuple, List

def validate_password_policy(password: str, policy) -> Tuple[bool, List[str]]:
    """
    Valida una contraseña contra una política de contraseñas

    :param password: contraseña en texto plano
    :param policy: instancia de PasswordPolicy (politicascontrasenas)
    :return: (is_valid, errores)
    """
    
    
    errors = []
    if not password:
        return False, ["La contraseña no puede estar vacía"]

    # Longitud mínima
    if len(password) < policy.min_length:
        errors.append(
            f"La contraseña debe tener al menos {policy.min_length} caracteres"
        )

    # Mayúsculas
    if policy.require_uppercase and not re.search(r"[A-Z]", password):
        errors.append("La contraseña debe contener al menos una letra mayúscula")

    # Minúsculas
    if policy.require_lowercase and not re.search(r"[a-z]", password):
        errors.append("La contraseña debe contener al menos una letra minúscula")

    # Números
    if policy.require_numbers and not re.search(r"[0-9]", password):
        errors.append("La contraseña debe contener al menos un número")

    # Caracter especial
    if policy.require_special_chars and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append(
            "La contraseña debe contener al menos un carácter especial"
        )

    return len(errors) == 0, errors
