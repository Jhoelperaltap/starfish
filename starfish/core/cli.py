import argparse
from starfish.core.app import App
from starfish.core.framework import runserver
from starfish.core.router import add_route, router
from starfish.middleware.logger import LoggerMiddleware
from starfish.middleware.auth import AuthMiddleware
from starfish.middleware.authorization import authorization_middleware
from starfish.core.templates import render_template
from starfish.core.websocket import start_websocket_server
from starfish.core.database import init_db, get_db_session
from starfish.core.cache import Cache
from starfish.core.celery import celery
from starfish.i18n import init_i18n, set_locale
from starfish.forms import LoginForm
from starfish.views import FileUploadView, FileDownloadView
from starfish.views import ItemListView, ItemCreateView, ItemUpdateView, ItemDeleteView
from starfish.core.middleware import middleware
from starfish.core.swagger import configure_swagger
from starfish.core.rate_limiting import configure_rate_limiting
from urllib.parse import parse_qs
from flask import Flask, request
import os
import sys

# Asegúrate de que config.py esté en el mismo directorio que cli.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import config
except ImportError as e:
    print(f"Error importing config module: {e}")
    sys.exit(1)

def home(request, session, *args):
    return render_template('home.html', {'title': 'Home'})

def about(request, session, *args):
    return render_template('about.html', {'title': 'About Starfish'})

def login(request, session, *args):
    content_length = int(request.headers['Content-Length']) if 'Content-Length' in request.headers else 0
    post_data = request.rfile.read(content_length) if content_length > 0 else b''
    form_data = {k: v[0] for k, v in parse_qs(post_data.decode()).items()}

    if request.command == 'POST':
        form = LoginForm(form_data)
        if form.validate():
            session['user'] = form_data['username']
            return "Login successful"
        else:
            return render_template('login.html', {'form': form})
    else:
        form = LoginForm()
        return render_template('login.html', {'form': form})

def api_example(request, session, *args):
    data = {
        "message": "Hello, API!",
        "user": session.get('user', 'Guest')
    }
    return data
def main():
    app = Flask(__name__)
    configure_swagger(app)
    configure_rate_limiting(app)

    parser = argparse.ArgumentParser(description='Starfish CLI')
    parser.add_argument('command', help='Subcommand to run')
    args = parser.parse_args()

    print(f"Command received: {args.command}")  # Mensaje de depuración

    cache = Cache(host=config.CACHE_HOST, port=config.CACHE_PORT, db=config.CACHE_DB)

    if args.command == 'runserver':
        print("Initializing database...")

        db_session_factory = init_db(config.DATABASE_URI)
        global db_session
        db_session = db_session_factory

        add_route("/", home)
        add_route("/about", about)
        add_route("/login", login)
        add_route("/api/example", api_example)

        # Añadir rutas para vistas CRUD
        add_route("/items", ItemListView().dispatch)
        add_route("/items/new", ItemCreateView().dispatch)
        add_route("/items/edit/(\\d+)", ItemUpdateView().dispatch)
        add_route("/items/delete/(\\d+)", ItemDeleteView().dispatch)

        # Añadir rutas para manejo de archivos
        add_route("/upload", FileUploadView().dispatch)
        add_route("/download/(.+)", FileDownloadView().dispatch)

        middleware.add_middleware(LoggerMiddleware())
        middleware.add_middleware(AuthMiddleware())
        middleware.add_middleware(authorization_middleware)

        app.run(debug=True, host='0.0.0.0', port=8000)
    elif args.command == 'runwebsocket':
        start_websocket_server()
    elif args.command == 'runtasks':
        celery.start()
    else:
        print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    main()
