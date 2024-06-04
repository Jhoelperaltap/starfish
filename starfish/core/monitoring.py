# starfish/core/monitoring.py

from prometheus_flask_exporter import PrometheusMetrics
from flask import Flask

def configure_monitoring(app: Flask):
    metrics = PrometheusMetrics(app)
    return app
