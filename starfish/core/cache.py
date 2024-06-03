import redis

class Cache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def set(self, key, value, ex=None):
        self.client.set(key, value, ex=ex)

    def get(self, key):
        return self.client.get(key)

    def delete(self, key):
        self.client.delete(key)

cache = Cache()
