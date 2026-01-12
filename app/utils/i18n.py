import gettext
from flask_jwt_extended import get_jwt_identity
_ = None
_current_lang = "es"  # idioma por defecto

def setup_gettext(lang_code='es', localedir='locales'):
    global _, _current_lang
    _current_lang = lang_code
    
    lang = gettext.translation('messages', localedir=localedir, languages=[lang_code], fallback=True)
    lang.install()
    _ = lang.gettext


def get_locale():
    """
        Retorna el idioma seleccionado por el usuario.
        Si el usuario no tiene uno definido, retorna el idioma por defecto ('es').
     """
    # 2. Fallback al idioma por defecto
    return _current_lang