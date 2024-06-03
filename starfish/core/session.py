# starfish/core/session.py

import os
import base64
from http.cookies import SimpleCookie
from datetime import datetime, timedelta

class Session:
    def __init__(self):
        self.sessions = {}

    def generate_sid(self):
        return base64.urlsafe_b64encode(os.urandom(24)).decode('utf-8')

    def get_session(self, request):
        if 'Cookie' in request.headers:
            cookie = SimpleCookie(request.headers['Cookie'])
            if 'sid' in cookie:
                sid = cookie['sid'].value
                if sid in self.sessions:
                    return self.sessions[sid]
        return None

    def create_session(self, response):
        sid = self.generate_sid()
        expires = datetime.utcnow() + timedelta(days=1)
        cookie = SimpleCookie()
        cookie['sid'] = sid
        cookie['sid']['path'] = '/'
        cookie['sid']['expires'] = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        response.headers['Set-Cookie'] = cookie.output(header='', sep='')
        self.sessions[sid] = {}
        return self.sessions[sid]

    def destroy_session(self, request, response):
        if 'Cookie' in request.headers:
            cookie = SimpleCookie(request.headers['Cookie'])
            if 'sid' in cookie:
                sid = cookie['sid'].value
                if sid in self.sessions:
                    del self.sessions[sid]
                cookie['sid']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
                response.headers['Set-Cookie'] = cookie.output(header='', sep='')

session_manager = Session()
