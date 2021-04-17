import os

API_URL = os.environ.get('API_URL', '127.0.0.1')
USER = os.environ.get('USER', 'test1')
INTERVAL = int(os.environ.get('INTERVAL', 1))

