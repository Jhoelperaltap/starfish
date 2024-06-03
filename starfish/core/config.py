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

