# -*- coding: utf-8 -*-

from datetime import datetime
from flask import (Blueprint, request, render_template, jsonify)

from etapi.kesseldata.helpers import (
    get_pellets_consumption_for_day,
    get_operating_hours_for_day,
    get_pellets_consumption_for_period,
    get_operating_hours_for_period,
    get_current_status,
    get_kessel_current_data,
    get_lager_current_data,
    get_puffer_current_data
)

from etapi.weather.helpers import (
    get_current_weather,
    get_average_temp_today,
    get_min_temp_today,
    get_max_temp_today,
)

from etapi.lib.helpers import (
    get_start_of_week,
    get_start_of_month,
    get_start_of_today
)


api = Blueprint('api', __name__, url_prefix='/api')

@api.route("/status")
def status():
    start_of_week = get_start_of_week()
    start_of_month = get_start_of_month()
    end_date = datetime.utcnow()
    today = get_start_of_today()
    data = {}

    data['status'] = get_current_status() or ''

    data['today'] = {}
    data['today']['pellets_consumption'] = get_pellets_consumption_for_day(today)
    data['today']['operating_hours'] = get_operating_hours_for_day(today)

    data['week'] = {}
    data['week']['pellets_consumption'] = get_pellets_consumption_for_period(start_of_week, end_date)
    data['week']['operating_hours'] = get_operating_hours_for_period(start_of_week, end_date)

    data['month'] = {}
    data['month']['pellets_consumption'] = get_pellets_consumption_for_period(start_of_month, end_date)
    data['month']['operating_hours'] = get_operating_hours_for_period(start_of_month, end_date)

    data['temp'] = {}
    data['temp']['current'] = get_current_weather().temp
    data['temp']['min'] = get_min_temp_today()
    data['temp']['max'] = get_max_temp_today()
    data['temp']['average'] = get_average_temp_today()

    return jsonify(data)


@api.route('/weather')
def weather():
    data = {}

    data['current'] = get_current_weather().temp
    data['min'] = get_min_temp_today()
    data['max'] = get_max_temp_today()
    data['average'] = get_average_temp_today()

    return jsonify(data)


@api.route('/pellets')
def pellets():
    kessel_data = get_kessel_current_data()
    lager_data = get_lager_current_data()
    start_of_week = get_start_of_week()
    start_of_month = get_start_of_month()
    end_date = datetime.utcnow()
    today = get_start_of_today()
    data = {}

    data['stock'] = lager_data.stock
    data['consumption_today'] = get_pellets_consumption_for_day(today)
    data['consumption_week'] = get_pellets_consumption_for_period(start_of_week, end_date)
    data['consumption_month'] = get_pellets_consumption_for_period(start_of_month, end_date)
    data['consumption_total'] = kessel_data.pellets_total

    return jsonify(data)


@api.route('/puffer')
def puffer():
    puffer_data = get_puffer_current_data()
    data = {}

    data['top'] = puffer_data.temperature_top
    data['bottom'] = puffer_data.temperature_bottom
    data['hot_water'] = puffer_data.hot_water_storage_temp

    return jsonify(data)
