import re
from jinja2 import Environment, FileSystemLoader

class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, path, handler):
        self.routes.append((re.compile(f"^{path}$"), handler))

    def match(self, path):
        for pattern, handler in self.routes:
            match = pattern.match(path)
            if match:
                return handler, match.groups()
        return None, None

router = Router()

def add_route(path, handler):
    router.add_route(path, handler)

def render_template(template_name, context):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    return template.render(context)
