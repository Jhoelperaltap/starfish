from http.cookies import SimpleCookie
from starfish.core.session import session_manager 

class AuthMiddleware:
    def process_request(self, request):
        if 'Cookie' in request.headers:
            cookie = SimpleCookie(request.headers['Cookie'])
            if 'sid' in cookie:
                sid = cookie['sid'].value
                if sid in session_manager.sessions:
                    request.session = session_manager.sessions[sid]
                    return
        request.session = {}

    def process_response(self, request, response):
        return response

auth_middleware = AuthMiddleware()
