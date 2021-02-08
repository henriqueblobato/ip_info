from settings import *
bind = f"0.0.0.0:{APP_PORT}"
workers = GUNICORN_WORKERS
threads = GUNICORN_THREADS
timeout = GUNICORN_TIMEOUT
limit_request_line = 4094
limit_request_fields = 16
limit_request_field_size = 8190