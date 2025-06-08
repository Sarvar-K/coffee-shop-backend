import os

wsgi_app = 'main:app'
bind = '0.0.0.0:8000'
reload = False
max_requests = os.getenv('WSGI_MAX_REQUESTS') or 10_000
max_requests_jitter = 10
log_level = os.getenv('WSGI_LOG_LEVEL') or 'ERROR'
timeout = os.getenv('WSGI_TIMEOUT') or 30
graceful_timeout = os.getenv('WSGI_GRACEFUL_TIMEOUT') or timeout
workers = os.getenv('WSGI_WORKERS') or 2
worker_class = 'uvicorn_worker.UvicornWorker'