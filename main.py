import os
import json
import re
import random
import threading
from multiprocessing import Pool, Process
from flask import Flask, render_template, request
import time

import settings
from settings import *
from geoip.geo import Geo
from rdap.rdap import Rdap
from tor.tor import Tor
from database import Redis

app = Flask(__name__, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16Mb

tor = Tor(settings)
geo = Geo(tor, settings)
rdap = Rdap(tor, settings)
redis = Redis(tor, settings)

@app.route('/')
def hello():
    public_ip = request.remote_addr
    if not public_ip=='127.0.0.1':
        result = handle(public_ip)
    else:
        result = {'ip':'', 'geolocation':'', 'rdap':''}
    
    return render_template('index2.html', port=APP_PORT, ip_info=result)


@app.route('/list', methods=['POST'])
def list_():
    if request.method == 'POST':
        ip = request.form['ipForm']
        if ip:
            result = handle(ip)
            print(result)
            return render_template('list2.html', ip_info=result)
        return render_template('list2.html', ip_info={})


def handle(ip):
    redis_geo = redis.get(f'{ip}geo')
    redis_rdap = redis.get(f'{ip}rdap')
    redis_is_tor = redis.get(f'{ip}tor')
    
    ip_dict = {'ip':ip}
    if redis_geo:
        # print('Redis found geo', ip)
        ip_dict['geolocation']=json.loads(redis_geo)
    else:
        geolocation = geo.get_geolocation(ip)
        ip_dict['geolocation']=geolocation
        if geolocation:
            status = redis.set(f'{ip}geo', json.dumps(geolocation))
    if redis_rdap:
        # print('Redis found rdap', ip)
        ip_dict['rdap'] = json.loads(redis_rdap)
    else:
        rdap_info = rdap.get_rdap(ip) # get whois
        ip_dict['rdap']=rdap_info
        if rdap_info:
            status = redis.set(f'{ip}rdap', json.dumps(rdap_info))
    if redis_is_tor:
        ip_dict['is_tor']=True
    else:
        ip_dict['is_tor']=False
    if not ip_dict['geolocation'] and not ip_dict['rdap']:
        return None
    return ip_dict

if __name__ == '__main__':
    app.run(debug=True, port=APP_PORT)