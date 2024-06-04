
from starfish.auth.roles import has_permission

class AuthorizationMiddleware:
    def process_request(self, request):
        session = request.session
        role = session.get('role', 'user')
        path = request.path
        method = request.command
        # Define permisos para cada ruta
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
