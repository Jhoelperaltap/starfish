# starfish/middleware/logger.py

class LoggerMiddleware:
    def process_request(self, request):
        print(f"Received request: {request.command} {request.path}")

    def process_response(self, request, response):
        print(f"Sending response: {response}")
        return response

logger_middleware = LoggerMiddleware()
