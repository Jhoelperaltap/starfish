import os
from starfish.core.views import View
from starfish.forms import ItemForm
from starfish.core.templates import render_template
from urllib.parse import parse_qs


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
    
UPLOAD_DIR = 'uoloads'

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
