import re
import os
import redis
import requests

class Redis():
    def __init__(self) -> None:
        self.host = os.getenv('REDIS_HOST', '127.0.0.1')
        self.port = os.getenv('REDIS_PORT', '6379')
        self.password = os.getenv('REDIS_PASSWORD', '')

        self.conn = redis.Redis(host=self.host,
                        port=self.port,
                        password=self.password)

        self.populate_with_tor_exit_nodes()

    def get(self, value):
        return self.conn.get(value)

    def set(self, key, values):
        return self.conn.set(key, str(values))

    def populate_with_tor_exit_nodes(self):
        response = requests.get('https://check.torproject.org/exit-addresses')
        tor_ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", response.text)
        for ip in tor_ips:
            self.conn.set(f'{ip}tor', 1)
        print('Update tor exit node with', len(tor_ips), 'ips')
        pass