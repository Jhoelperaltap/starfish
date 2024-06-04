from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
from flask import Flask, request

def configure_rate_limiting(app: Flask):
    # Configura la conexión a Redis
    redis_client = Redis(host='localhost', port=6379)

    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="redis://localhost:6379"
    )
    limiter.init_app(app)  
    return app

app = Flask(__name__)
configure_rate_limiting(app)

if __name__ == "__main__":
    app.run(port=8000)

