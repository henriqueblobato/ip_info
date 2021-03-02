import re
import redis

class Redis():
    def __init__(self, tor_instance, settings) -> None:
        self.host = settings.REDIS_HOST
        self.port = settings.REDIS_PORT
        self.password = settings.REDIS_PASSWORD

        self.tor_instance = tor_instance

        self.conn = redis.Redis(host=self.host,
                        port=self.port,
                        password=self.password)

        self.settings = settings
        self.populate_with_tor_exit_nodes()

    def get(self, value):
        return self.conn.get(value)

    def set(self, key, values):
        return self.conn.set(key, str(values))

    def populate_with_tor_exit_nodes(self):
        response = self.tor_instance.session.get('https://check.torproject.org/exit-addresses')
        tor_ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", response.text)
        for ip in tor_ips:
            # self.conn.set(f'{ip}tor', 1)
            self.settings.TOR_IPS.append(ip)
        print('\n[!] Update tor exit node with', len(tor_ips), 'ips')
        pass