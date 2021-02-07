import datetime
import requests

class Geo:

    def __init__(self, tor_instance):
        self.tor_instance = tor_instance

    def get_geolocation(self, ip):
        url = f'https://ipinfo.io/{ip}'
        response, status = self.tor_instance.get(url)
        if status!=200 or 'bogon' in response.keys():
            return {}
        try:
            response['org'] = ' '.join(response['org'].split()[1:])
        except Exception as e:
            print('org error', ip, format(e), type(e))
        try:
            time_there = self.tor_instance.get((f'http://worldtimeapi.org/api/timezone/{response.get("timezone")}'))
            time_there = datetime.datetime.fromisoformat(time_there[0].get('datetime')).strftime('%D %H:%M:%S')
            response['timezone_formated'] = time_there
        except Exception as e:
            print('timezone error', ip, format(e), type(e))
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
