
from flask_wtf.csrf import CSRFProtect
from flask import Flask

def configure_csrf(app: Flask):
    csrf = CSRFProtect()
    csrf.init_app(app)
    return app
