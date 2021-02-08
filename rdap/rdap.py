import requests
import json

class Rdap():

    def __init__(self, tor_instance, settings):
        self.tor_instance = tor_instance
        self.settings = settings

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
