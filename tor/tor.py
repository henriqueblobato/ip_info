import ast
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
        current_ip = self.session.get('http://ifconfig.me').text
        print('Using public ip:', current_ip)

    def get(self, url):
        for i in range(3):
            try:
                response = self.session.get(url, timeout=5)
                js = response.json()
                if 'error' in js.keys():
                    with Controller.from_port(port = 9051) as controller:
                        controller.authenticate(password='henrique')
                        controller.signal(Signal.NEWNYM)
                        print('Tor ip changed')
                    continue
                return response.json(), response.status_code
            except Exception as e:
                pass