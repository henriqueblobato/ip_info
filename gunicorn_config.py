from settings import APP_PORT
bind = f"0.0.0.0:{APP_PORT}"
workers = 8
threads = 32
timeout = 30
limit_request_line = 4094
limit_request_fields = 20
limit_request_field_size = 8190