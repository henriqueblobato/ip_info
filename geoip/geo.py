import datetime
import requests

class Geo:

    def __init__(self, tor_instance, settings):
        self.tor_instance = tor_instance
        self.settings = settings

    def get_geolocation(self, ip):
        url = self.settings.IP_GEOLOCATION_URL
        url = url.format(ip) #f'https://ipinfo.io/{ip}'
        response, status = self.tor_instance.get(url)
        if status!=200 or 'bogon' in response.keys():
            return {}
        try:
            response['org'] = ' '.join(response['org'].split()[1:])
        except KeyError as ke:
            pass
        try:
            url = self.settings.TIMEZONE_URL
            url = url.format(response.get("timezone"))
            time_there = self.tor_instance.get(url)
            time_there = datetime.datetime.fromisoformat(time_there[0].get('datetime')).strftime(self.settings.CLOCK_FORMAT)
            response['timezone_formated'] = time_there
        except Exception as e:
            pass
        return response

# class GeoModel:
#     def __init__(self):
#         self.ip = '148.5.133.202'
#         self.city = 'Santa Clara'
#         self.region = 'California'
#         self.country = 'US'
#         self.loc = '37.3483,-121.9844'
#         self.postal = '95051'
#         self.timezone = 'America/Los_Angeles'
#         self.readme = 'https://ipinfo.io/missingauth'
