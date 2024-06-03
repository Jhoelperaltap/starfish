from babel import Locale

babel = Locale('en', 'US')

def init_i18n(app):
    babel.init_app(app)

def set_locale(locale):
    babel.locale_selector_func = lambda: locale
