import requests
import json
import sys
import socket

class Rdap():

    def __init__(self, tor_instance, settings):
        self.tor_instance = tor_instance
        self.settings = settings

    def get_whois(self, ip) -> dict:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("whois.arin.net", 43))
        s.send((ip + "\r\n").encode())

        response = b""
        while True:
            data = s.recv(4096)
            response += data
            if not data:
                break
        s.close()
        response = response.decode().split('\n')

        response = [i.strip() for i in response]
        d = {}
        for line in response:
            if not line.startswith('#') and ':' in line:
                try:
                    name, value = line.split(':')
                    if value:
                        d[name] = value.strip()
                except:
                    continue
            else:
                continue

        return d

    def get_rdap(self, ip) -> dict:
        try:
            url = self.settings.IP_RDAP_INFO
            url = url.format(ip)
            response, status = self.tor_instance.get(url)
            if 'remarks' in response.keys():
                response['address'] = ' '.join(response['remarks'][0]['description'])
            if status!=200:
                raise Exception
            return response
        except:
            return {}

