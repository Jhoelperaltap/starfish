# # Starfish Framework Documentation

## Overview
Starfish is a lightweight web framework designed to be flexible and extensible. It includes support for middleware, form handling, CRUD operations, WebSockets, file handling, and advanced authentication and authorization.


## Table of Contents

1. Getting Started
2. Project Structure
3. Routing
4. Middleware
5. Forms
6. Views
7. Authentication and Authorization

## Getting Started

To get started with Starfish, clone the repository and set up your virtual environment:
git clone <[Jhoelperaltap/starfish (github.com)](https://github.com/Jhoelperaltap/starfish)>
cd starfish
python -m venv starfish-env
starfish-env\Scripts\activate
pip install -r requirements.txt

## Project Structure
The project structure for Starfish is organized as follows:
starfish
│
├── starfish
│   ├── core
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── cli.py
│   │   ├── framework.py
│   │   ├── router.py
│   │   ├── views.py
│   │   ├── session.py
│   │   ├── websocket.py
│   │   ├── middleware.py
│   ├── forms.py
│   ├── middleware
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── logger.py
│   ├── templates
│   │   ├── home.html
│   │   ├── about.html
│   │   ├── login.html
│   │   ├── item_list.html
│   │   ├── item_form.html
│   │   ├── upload_form.html
│   ├── views.py
├── config.py
├── starfish-env
├── requirements.txt


## Routing

Routes are defined in the `cli.py` file using the `add_route` function. Here's an example of how to define routes:
from starfish.core.router import add_route

    def main():
        add_route("/", home)
        add_route("/about", about)
        add_route("/login", login)
        add_route("/api/example", api_example)
        add_route("/items", ItemListView().dispatch)
        add_route("/items/new", ItemCreateView().dispatch)
        add_route("/items/edit/(\\d+)", ItemUpdateView().dispatch)
        add_route("/items/delete/(\\d+)", ItemDeleteView().dispatch)
        add_route("/upload", FileUploadView().dispatch)
        add_route("/download/(.+)", FileDownloadView().dispatch)

## Middleware
Middleware allows you to process requests and responses. Middleware is added using the `middleware.add_middleware` function.

### Example Middleware

#### Logger Middleware

# starfish/middleware/logger.py

class LoggerMiddleware:
    def process_request(self, request):
        print(f"Received request: {request.command} {request.path}")

    def process_response(self, request, response):
        print(f"Sending response: {response}")
        return response

    logger_middleware = LoggerMiddleware()

#### Authorization Middleware


    from starfish.auth.roles import has_permission
    
    class AuthorizationMiddleware:
        def process_request(self, request):
            session = request.session
            role = session.get('role', 'user')
            path = request.path
            method = request.command
            permissions = {
                'GET': {
                    '/items': 'view_items',
                    '/items/new': 'add_item',
                    '/items/edit': 'edit_item',
                    '/items/delete': 'delete_item'
                },
                'POST': {
                    '/items': 'view_items',
                    '/items/new': 'add_item',
                    '/items/edit': 'edit_item',
                    '/items/delete': 'delete_item'
                }
            }
            permission = permissions.get(method, {}).get(path)
            if permission and not has_permission(role, permission):
                return {
                    'status': 403,
                    'body': 'Forbidden',
                    'content_type': 'text/plain'
                }
            return None
    
        def process_response(self, request, response):
            return response
    
    authorization_middleware = AuthorizationMiddleware()
    
## Forms

Forms are handled using WTForms. Define your forms in `forms.py`.

### Example Form

    from wtforms import Form, StringField, validators
    
    class ItemForm(Form):
        name = StringField('Name', [validators.InputRequired()])
        description = StringField('Description', [validators.InputRequired()])

## Views

    from starfish.core.views import View
    from starfish.forms import ItemForm
    from starfish.core.templates import render_template
    
    database = {}
    
    class ItemListView(View):
        def get(self, request, session, *args):
            items = database.values()
            return render_template('item_list.html', {'items': items})
    
    class ItemCreateView(View):
        def get(self, request, session, *args):
            form = ItemForm()
            return render_template('item_form.html', {'form': form})
    
        def post(self, request, session, *args):
            content_length = int(request.headers['Content-Length']) if 'Content-Length' in request.headers else 0
            post_data = request.rfile.read(content_length) if content_length > 0 else b''
            form_data = {k: v[0] for k, v in parse_qs(post_data.decode()).items()}
            form = ItemForm(form_data)
            if form.validate():
                item_id = len(database) + 1
                database[item_id] = {'id': item_id, 'name': form.name.data, 'description': form.description.data}
                return "Item created successfully"
            return render_template('item_form.html', {'form': form})
    
    class ItemUpdateView(View):
        def get(self, request, session, item_id, *args):
            item = database.get(int(item_id))
            if not item:
                return "Item not found"
            form = ItemForm(data=item)
            return render_template('item_form.html', {'form': form, 'item_id': item_id})
    
        def post(self, request, session, item_id, *args):
            item = database.get(int(item_id))
            if not item:
                return "Item not found"
            content_length = int(request.headers['Content-Length']) if 'Content-Length' in request.headers else 0
            post_data = request.rfile.read(content_length) if content_length > 0 else b''
            form_data = {k: v[0] for k, v in parse_qs(post_data.decode()).items()}
            form = ItemForm(form_data)
            if form.validate():
                item.update({'name': form.name.data, 'description': form.description.data})
                return "Item updated successfully"
            return render_template('item_form.html', {'form': form, 'item_id': item_id})
    
    class ItemDeleteView(View):
        def post(self, request, session, item_id, *args):
            if int(item_id) in database:
                del database[int(item_id)]
                return "Item deleted successfully"
            return "Item not found"


## Authentication and Authorization

Authentication is managed using middleware. You can define roles and permissions to restrict access to certain routes.
    
### Example Roles and Permissions 
    
    class Role:
        ADMIN = 'admin'
        USER = 'user'
    
    roles_permissions = {
        Role.ADMIN: ['view_items', 'add_item', 'edit_item', 'delete_item'],
        Role.USER: ['view_items']
    }
    
    def has_permission(role, permission):
        return permission in roles_permissions.get(role, [])

## File Handling
You can handle file uploads and downloads using dedicated views.

### Example File Handling Views

There are two types of synchronization and they can complement each other:

    import os
    from starfish.core.views import View
    from starfish.core.templates import render_template
    
    UPLOAD_DIR = 'uploads'
    
    class FileUploadView(View):
        def get(self, request, session, *args):
            return render_template('upload_form.html', {})
    
        def post(self, request, session, *args):
            content_length = int(request.headers['Content-Length']) if 'Content-Length' in request.headers else 0
            post_data = request.rfile.read(content_length) if content_length > 0 else b''
            filename = request.headers['filename']
    
            with open(os.path.join(UPLOAD_DIR, filename), 'wb') as f:
                f.write(post_data)
    
            return "File uploaded successfully"
    
    class FileDownloadView(View):
        def get(self, request, session, filename, *args):
            filepath = os.path.join(UPLOAD_DIR, filename)
            if not os.path.exists(filepath):
                return "File not found"
            
            with open(filepath, 'rb') as f:
                file_content = f.read()
    
            response = {
                'status': 200,
                'body': file_content,
                'content_type': 'application/octet-stream'
            }
            return response

## WebSockets

Starfish supports WebSockets for real-time communication.


    import asyncio
    import websockets
    
    clients = set()
    
    async def register(websocket):
        clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            clients.remove(websocket)
    
    async def ws_handler(websocket, path):
        await register(websocket)
        async for message in websocket:
            for client in clients:
                if client != websocket:
                    await client.send(message)
    
    def start_websocket_server():
        loop = asyncio.get_event_loop()
        server = websockets.serve(ws_handler, "localhost", 8765)
        loop.run_until_complete(server)
        loop.run_forever()

## APIs

Starfish allows you to create RESTful APIs easily.

### Example API Route


    def api_example(request, session, *args):
        data = {
            "message": "Hello, API!",
            "user": session.get('user', 'Guest')
        }
        return data

## Running the Server

    starfish runserver
To run the WebSocket server, use:

    starfish runwebsocket
