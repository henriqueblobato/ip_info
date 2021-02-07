import requests
import json

class Rdap():

    def __init__(self, tor_instance):
        self.tor_instance = tor_instance

    def get_rdap(self, ip) -> dict:
        try:
            url = f'http://rdap.apnic.net/ip/{ip}'
            response, status = self.tor_instance.get(url)
            if 'remarks' in response.keys():
                response['address'] = ' '.join(response['remarks'][0]['description'])
            if status!=200:
                raise Exception
            return response
        except:
            return {}
