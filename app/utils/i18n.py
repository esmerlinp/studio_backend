import gettext

_ = None

def setup_gettext(lang_code='es', localedir='locales'):
    global _
    lang = gettext.translation('messages', localedir=localedir, languages=[lang_code], fallback=True)
    lang.install()
    _ = lang.gettext
