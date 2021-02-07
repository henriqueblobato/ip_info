import os

# WEB APPLICATION
APP_PORT = 8080

# Upload safety
ALLOWED_EXTENSIONS = {'txt'}
CONTENT_TYPE_ALLOWED = ['text/plain']

# Threading
WORKERS = int(os.getenv('THREAD_WORKERS', 2**4))

# Redis
HOST = os.getenv('REDIS_HOST', '172.16.0.101')
PORT = os.getenv('REDIS_PORT', '6379')
PASSWORD = os.getenv('REDIS_PASSWORD', '')

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
HTTP_RETRIES = 3