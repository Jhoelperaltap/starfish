import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from starfish.core.middleware import middleware
from starfish.core.router import router, render_template
from starfish.core.session import session_manager

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def handle_request(self):
        try:
            response = middleware.process_request(self)
            if response:
                self.send_response(response['status'])
                self.send_header('Content-type', response.get('content_type', 'text/html'))
                self.end_headers()
                self.wfile.write(response['body'].encode())
                return

            handler, args = router.match(self.path)
            if handler:
                session = session_manager.get_session(self)
                if not session:
                    session = session_manager.create_session(self)
                response = handler(self, session, *args)
                response = middleware.process_response(self, response)
                if isinstance(response, dict):  # Check if the response is JSON
                    response = json.dumps(response)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not Found")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")
            print(f"Error processing request: {e}")

def runserver():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting server on port 8000...")
    httpd.serve_forever()
