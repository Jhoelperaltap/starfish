
from flasgger import Swagger
from flask import Flask

def configure_swagger(app: Flask):
    swagger = Swagger(app)

    # Configuración de Swagger
    app.config['SWAGGER'] = {
        'title': 'Starfish API',
        'uiversion': 3
    }

    return app
