
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
from urllib.parse import parse_qs
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

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
    parser = argparse.ArgumentParser(description='Starfish CLI')
    parser.add_argument('command', help='Subcommand to run')
    args = parser.parse_args()

    cache = Cache(host=config.CACHE_HOST,
                  port=config.CACHE_PORT,
                  db=config.CACHE_DB)

    if args.command == 'runserver':
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
        
        add_route("/upload", FileUploadView().dispatch)
        add_route("/download/(.+)", FileDownloadView().dispatch)

        middleware.add_middleware(LoggerMiddleware())
        middleware.add_middleware(AuthMiddleware())
        middleware.add_middleware(authorization_middleware)

        runserver()
    elif args.command == 'runwebsocket':
        start_websocket_server()
    elif args.command == 'runtasks':
        celery.start()
    else:
        print(f"Unknown command: {args.command}")
