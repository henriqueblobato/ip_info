from time import sleep
import requests
from stem import Signal
from stem.control import Controller
import os

from settings import *

class Tor:

    def __init__(self, settings):
        self.session = requests.session()
        if settings.USE_TOR: # bypass daily request limit
            self.session.proxies = {'http':'socks5://127.0.0.1:9050','https':'socks5://127.0.0.1:9050'}
        self.current_ip = self.get_ip()
        self.ip_lock = False

    def get_ip(self):
        response = self.session.get('http://ifconfig.me', timeout=3).text
        # print('[!] Using public ip:', response)
        return response
    
    def get(self, url):
        for i in range(3):
            try:
                response = self.session.get(url, timeout=5)
                js = response.json()
                if 'error' in js.keys():
                    old_ip = self.current_ip
                    if not self.ip_lock:
                        self.ip_lock = True
                        with Controller.from_port(port = 9051) as controller:
                            controller.authenticate(password='henrique')
                            controller.signal(Signal.NEWNYM)
                            self.current_ip = self.get_ip()
                        self.ip_lock = False
                        sleep(3)
                    continue
                return response.json(), response.status_code
            except Exception as e:
                return None, None
