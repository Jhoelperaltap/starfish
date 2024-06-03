
class Role:
    ADMIN = 'admin'
    USER = 'user'

roles_permissions = {
    Role.ADMIN: ['view_items', 'add_item', 'edit_item', 'delete_item'],
    Role.USER: ['view_items']
}

def has_permission(role, permission):
    return permission in roles_permissions.get(role, [])
