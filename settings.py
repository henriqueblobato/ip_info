import os

# WEB APPLICATION
APP_PORT = 80

# Upload safety
ALLOWED_EXTENSIONS = {'txt'}
CONTENT_TYPE_ALLOWED = ['text/plain']

# Threading
WORKERS = int(os.getenv('THREAD_WORKERS', 1))
GUNICORN_WORKERS = int(os.getenv('GUNICORN_WORKERS', 1))
GUNICORN_THREADS = int(os.getenv('GUNICORN_THREADS', 16))
GUNICORN_TIMEOUT = int(os.getenv('GUNICORN_TIMEOUT', 60))

# Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

# URLs
IP_GEOLOCATION_URL = 'https://ipinfo.io/{}'
IP_RDAP_INFO = 'http://rdap.apnic.net/ip/{}'

# TIMEZONE
TIMEZONE_URL = 'http://worldtimeapi.org/api/timezone/{}'
CLOCK_FORMAT = '%D %H:%M:%S'

# USE TOR NETWORK
USE_TOR = bool(os.getenv('USE_TOR', False))
TOR_HASHED_PASSWORD = os.getenv('TOR_HASHED_PASSWORD', 'henrique')

# RETRIES NUMBER BEFORE RETURN NONE
HTTP_RETRIES = int(os.getenv('HTTP_RETRIES', 3))

TOR_IPS = []