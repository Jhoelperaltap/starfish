
class MiddlewareManager:
    def __init__(self):
        self._middlewares = []

    def add_middleware(self, middleware):
        self._middlewares.append(middleware)

    def process_request(self, request):
        for middleware in self._middlewares:
            if hasattr(middleware, 'process_request'):
                response = middleware.process_request(request)
                if response:
                    return response
        return None

    def process_response(self, request, response):
        for middleware in reversed(self._middlewares):
            if hasattr(middleware, 'process_response'):
                response = middleware.process_response(request, response)
        return response

middleware = MiddlewareManager()
