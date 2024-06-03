# starfish/core/app.py

class App:
    def __init__(self):
        self.config = {}
        self.cache = None
        self.db_session = None
        self.router = None
        self.middleware = []

    def add_middleware(self, middleware):
        self.middleware.append(middleware)

    def set_config(self, config):
        self.config = config

    def set_cache(self, cache):
        self.cache = cache

    def set_db_session(self, db_session):
        self.db_session = db_session

    def set_router(self, router):
        self.router = router
