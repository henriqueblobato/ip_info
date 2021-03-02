import requests
import re
from flask import Flask, render_template, request

import settings
from settings import *
from geoip.geo import Geo
from rdap.rdap import Rdap
from tor.tor import Tor

app = Flask(__name__, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16Mb

tor = Tor(settings)
geo = Geo(tor, settings)
rdap = Rdap(tor, settings)

ip_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
response = requests.get('https://check.torproject.org/exit-addresses')
tor_ips = re.findall(ip_regex, response.text)
for ip in tor_ips:
    settings.TOR_IPS.append(ip)
print('\n[!] Updated tor exit node with', len(tor_ips), 'ips')

@app.route('/', methods=['POST', 'GET'])
def root():
    
    result = {'ip':'', 'geolocation':'', 'rdap':'', 'whois': ''}
    show_your_ip=False

    if request.method == 'POST':        
        public_ip = request.form['ipForm']
    
    if request.method == 'GET':    
        public_ip = request.headers.get('X-Forwarded-For')
        print('[!] REQUEST FROM', public_ip)
        show_your_ip=True
    
    if public_ip and re.match(ip_regex,public_ip):# and not request.remote_addr == '127.0.0.1': # dev env
        result = handle(public_ip)
        
    return render_template('index2.html', port=APP_PORT, ip_info=result, public_ip=public_ip, show_your_ip=show_your_ip)


def handle(ip):

    ip_dict = {'ip':ip}
    try:
        geolocation = geo.get_geolocation(ip)
        ip_dict['geolocation'] = geolocation
        print('geolocation --->', geolocation)
    except Exception as e:
        ip_dict['geolocation'] = {}
        print('[Error geolocation]', format(e), type(e))

    try:
        rdap_info = rdap.get_rdap(ip) # get whois
        ip_dict['rdap'] = rdap_info
    except Exception as e:
        ip_dict['rdap'] = {}
        print('[Error rdap]', format(e), type(e))

    try:
        whois_info = rdap.get_whois(ip) # get whois    
        ip_dict['whois'] = whois_info
    except Exception as e:
        ip_dict['whois'] = {}
        print('[Error whois]', format(e), type(e))


    ip_dict['is_tor'] = True if ip in settings.TOR_IPS else False

    if not ip_dict['geolocation'] and not ip_dict['rdap']:
        return None
    
    return ip_dict

if __name__ == '__main__':
    app.run(debug=True, port=APP_PORT)