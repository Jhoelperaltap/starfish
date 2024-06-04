import os

class Config:
    def __init__(self):
        self.settings = {}

    def from_envvar(self, key):
        value = os.getenv(key)
        if value:
            self.settings[key] = value

    def from_pyfile(self, filename):
        with open(filename) as config_file:
            exec(config_file.read(), self.settings)

config = Config()


DATABASE_URI = 'sqlite:///starfish.db'
CACHE_HOST = 'localhost'
CACHE_PORT = 6379
CACHE_DB = 0
LOCALE_DIR = 'locales'
DEFAULT_LOCALE = 'en'
