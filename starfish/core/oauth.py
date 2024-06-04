
from flask_oauthlib.provider import OAuth2Provider
from flask import Flask

def configure_oauth(app: Flask):
    oauth = OAuth2Provider(app)
    return app
