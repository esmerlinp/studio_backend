import re
from typing import Tuple, List
from app.utils import i18n
def validate_password_policy(password: str, policy) -> Tuple[bool, List[str]]:
    """
    Valida una contraseña contra una política de contraseñas

    :param password: contraseña en texto plano
    :param policy: instancia de PasswordPolicy (politicascontrasenas)
    :return: (is_valid, errores)
    """
    
    
    errors = []
    if not password:
        return False, [i18n._("error.password.empty")]

    # Longitud mínima
    if len(password) < policy.min_length:
        msg = i18n._("error.password.min_length") % policy.min_length
        errors.append(msg)

    # Mayúsculas
    if policy.require_uppercase and not re.search(r"[A-Z]", password):
        errors.append(i18n._("error.password.require_uppercase"))

    # Minúsculas
    if policy.require_lowercase and not re.search(r"[a-z]", password):
       errors.append(i18n._("error.password.require_lowercase"))

    # Números
    if policy.require_numbers and not re.search(r"[0-9]", password):
        errors.append(i18n._("error.password.require_numbers"))

    # Caracter especial
    if policy.require_special_chars and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append(i18n._("error.password.require_special"))

    return len(errors) == 0, errors
