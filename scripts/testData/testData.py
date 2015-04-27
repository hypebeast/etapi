# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import random

def daterange(start_date, end_date, delta):
    curr = start_date
    while curr < end_date:
        yield curr
        curr += delta

def createWeatherData(start_date=datetime.utcnow() - timedelta(days=7),
                        end_date=datetime.utcnow(), min_temp=-10.0, max_temp=40.0):
    data = []
    for x in daterange(start_date, end_date, timedelta(minutes=5)):
        data.append({'date': x, 'value': random.uniform(min_temp, max_temp)})

    return data

def createKesselData(start_date=datetime.utcnow() - timedelta(days=7),
                        end_date=datetime.utcnow()):
    data = []
    pellets_total = 2000
    operating_hours = 143 * 24 * 60 * 60
    for x in daterange(start_date, end_date, timedelta(minutes=5)):
        pellets_total += 1
        pellets_stock = int(random.uniform(0, 60))
        operating_hours += 300
        data.append({'date': x, 'pellets_total': pellets_total, 'pellets_stock': pellets_stock, 'operating_hours': int(operating_hours/3600)})

    return data

def createLagerData(start_date=datetime.utcnow() - timedelta(days=7),
                        end_date=datetime.utcnow()):
    data = []
    stock = 10000.0
    delta = 0.1
    for x in daterange(start_date, end_date, timedelta(minutes=5)):
        stock -= delta
        data.append({'date': x, 'stock': int(stock)})

    return data

if __name__ == '__main__':
    data = createWeatherData()
    print data
