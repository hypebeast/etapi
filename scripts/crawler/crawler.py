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
from etapi.kesseldata.models import Kessel, Lager

if os.environ.get("ETAPI_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

API_HOST = "http://192.168.0.108"
API_PORT = "8080"

def getStrValueOrNone(xml):
    doc = xmltodict.parse(xml)
    if doc["eta"]["value"]["@strValue"]:
        return doc["eta"]["value"]["@strValue"]

    return None

def getValueOrNone(xml):
    doc = xmltodict.parse(xml)
    if doc["eta"]["value"]:
        return doc["eta"]["value"]

    return None

def apiCall(resource_url="/user/api/"):
    url = API_HOST + ":" + API_PORT + resource_url
    r = requests.get(url)
    r.encoding = "UTF-8"
    return r

def getUserVar(var):
    var_url = "/user/var" + var
    return apiCall(var_url).text

def kesselData():
    vollaststunden = int(getValueOrNone("/40/10021/0/0/12153"))
    gesamtverbrauch = int(getStrValueOrNone("/40/10021/0/0/12016"))
    verbrauchseitwartung = int(getValueOrNone("/40/10021/0/0/12014"))
    behaelterinhalt = int(getStrValueOrNone("/40/10021/0/0/12011"))
    verbrauchseitentaschung = int(getStrValueOrNone("/40/10021/0/0/12012"))
    verbrauchseitascheboxleeren = int(getStrValueOrNone("/40/10021/0/0/12013"))

    kessel = Kessel(operating_hours=vollaststunden,
                    pellets_total=gesamtverbrauch,
                    usage_since_service=verbrauchseitwartung,
                    reservoir_capacity=behaelterinhalt,
                    usage_since_deashing=verbrauchseitentaschung,
                    usage_since_box_exhaustion=verbrauchseitascheboxleeren)

    with app.app_context():
        db.session.add(kessel)
        db.session.commit()

def lagerData():
    lager_vorrat = getStrValueOrNone(getUserVar("/40/10201/0/0/12015"))
    lager = Lager(stock=int(lager_vorrat))
    with app.app_context():
        db.session.add(lager)
        db.session.commit()

def weatherData():
    data = getUserVar("")
    doc = xmltodict.parse(data)
    temp = getStrValueOrNone("/40/10241/0/0/12197")
    if temp:
        temp = float(temp.replace(',', '.'))
        weather = Weather(temp=temp)
        with app.app_context():
            db.session.add(weather)
            db.session.commit()

def main():
    start = datetime.utcnow()
    print "%s - Start crawling" % (start.strftime('%Y-%m-%d %H:%M:%S'))

    weatherData()
    kesselData()
    lagerData()

    end = datetime.utcnow()
    print "%s - DONE" % ((end.strftime('%Y-%m-%d %H:%M:%S')))

def exit():
    sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
