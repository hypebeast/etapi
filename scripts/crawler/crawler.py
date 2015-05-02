#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from datetime import datetime

import requests
import xmltodict

from etapi.app import create_app
from etapi.extensions import db
from etapi.settings import DevConfig, ProdConfig
from etapi.weather.models import Weather

if os.environ.get("ETAPI_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

ctx = app.app_context()

API_HOST = "http://192.168.0.108"
API_PORT = "8080"

def apiCall(resource_url="/user/api/"):
    url = API_HOST + ":" + API_PORT + resource_url
    r = requests.get(url)
    r.encoding = "UTF-8"
    return r

def getUserVar(var):
    var_url = "/user/var" + var
    return apiCall(var_url).text

def kesselData():
    pass

def lagerData():
    pass

def weatherData():
    data = getUserVar("/40/10241/0/0/12197")
    doc = xmltodict.parse(data)
    if doc["eta"]["value"]["@strValue"]:
        temp = doc["eta"]["value"]["@strValue"]
        temp = float(temp.replace(',', '.'))
        weather = Weather(temp=temp)
        with app.app_context():
            db.session.add(weather)
            db.session.commit()


def main():
    start = datetime.utcnow()
    print "%s - Start crawling..." % (start.strftime('%Y-%m-%d %H-%M-%S'))

    weatherData()
    kesselData()
    lagerData()

    end = datetime.utcnow()
    print "%s - DONE" % ((end.strftime('%Y-%m-%d %H-%M-%S')))

def exit():
    sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
