#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand

from etapi.app import create_app
from etapi.user.models import User
from etapi.weather.models import Weather
from etapi.kesseldata.models import Kessel, Lager
from etapi.settings import DevConfig, ProdConfig
from etapi.database import db
from scripts.testData import createWeatherData, createKesselData, createLagerData

if os.environ.get("ETAPI_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)

def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}

@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

@manager.command
def loadtestdata():
    with app.app_context():
        weather_data = createWeatherData()
        for x in weather_data:
            print x['date']
            print x['value']
            weather = Weather(temp=x['value'], created_at=x['date'])
            db.session.add(weather)

        kessel_data = createKesselData()
        for x in kessel_data:
            data = Kessel(created_at=x['date'],
                            pellets_total=x['pellets_total'],
                            pellets_stock=x['pellets_stock'],
                            operating_hours=x['operating_hours'])
            db.session.add(data)

        lager_data = createLagerData()
        for x in lager_data:
            data = Lager(created_at=x['date'],
                            stock=x['stock'])
            with app.app_context():
                db.session.add(data)

        db.session.commit()

@manager.command
def resetdb():
    db.drop_all()
    db.create_all()

@manager.command
def dropdb():
    db.drop_all()

@manager.command
def createdb():
    db.create_all()

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
