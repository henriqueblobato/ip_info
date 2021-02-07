import os
import json
import re
import random
from multiprocessing import Pool
from flask import Flask, render_template, request

import settings
from settings import *
from geoip.geo import Geo
from rdap.rdap import Rdap
from tor.tor import Tor
from database import Redis

app = Flask(__name__, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16Mb

# ALLOWED_EXTENSIONS = {'txt'}
# CONTENT_TYPE_ALLOWED = ['text/plain']
# WORKERS = int(os.getenv('THREAD_WORKERS', 2**4))

tor = Tor(settings)
geo = Geo(tor)
rdap = Rdap(tor)
redis = Redis()

@app.route('/')
def hello():
    return render_template('index.html', port=APP_PORT)

@app.route('/list', methods = ['POST'])
def list_():
    if request.method == 'POST':
      f = request.files['file']
      if f.mimetype not in CONTENT_TYPE_ALLOWED and f.filename.split('.')[-1] not in ALLOWED_EXTENSIONS:
          return 'Please insert a valid file'
      content = f.read()
      content = content.decode('utf-8').split('\n')
      
      ip_list = []
      for line in content:
        ips_candidate = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
        if not ips_candidate: continue
        if len(ips_candidate)>1:
            ip_list.extend(ips_candidate)
        else:
            ip_list.append(ips_candidate[0])

      ips_info = []
      r = random.randint(500, 4900)
      ip_list = list(set(ip_list[r:r+50]))
      with Pool(WORKERS) as p:
        result = p.map(handle, ip_list)
    result = [i for i in result if i is not None]
    return render_template('list.html', ips_info=result)

def handle(ip):
    redis_geo = redis.get(f'{ip}geo')
    redis_rdap = redis.get(f'{ip}rdap')
    redis_is_tor = redis.get(f'{ip}tor')
    
    ip_dict = {'ip':ip}
    if redis_geo:
        print('Found geo', ip)
        ip_dict['geolocation']=json.loads(redis_geo)
    else:
        geolocation = geo.get_geolocation(ip)
        ip_dict['geolocation']=geolocation
        status = db_set(f'{ip}geo', json.dumps(geolocation))
    if redis_rdap:
        print('Found rdap', ip)
        ip_dict['rdap']=json.loads(redis_rdap)
    else:
        rdap_info = rdap.get_rdap(ip)
        ip_dict['rdap']=rdap_info
        status = db_set(f'{ip}rdap', json.dumps(rdap_info))
    if redis_is_tor:
        ip_dict['is_tor']=True
    else:
        ip_dict['is_tor']=False
    if not ip_dict['geolocation'] and not ip_dict['rdap']:
        return None
    return ip_dict

def db_set(ip, values):
    response = redis.set(ip, values)
    return response

if __name__ == '__main__':
    app.run(debug=True)