# -*- coding: utf-8 -*-
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)

from etapi.database import db
from etapi.weather.helpers import get_current_weather, get_max_temp_today, get_min_temp_today, get_average_temp_today
from etapi.kesseldata.helpers import get_pellets_consumption_today
from etapi.kesseldata.helpers import get_pellets_consumption_last_n_days
from etapi.kesseldata.helpers import get_kessel_current_data
from etapi.kesseldata.helpers import get_puffer_current_data
from etapi.kesseldata.helpers import get_lager_current_data
from etapi.kesseldata.helpers import get_operating_hours_last_n_days


public = Blueprint('public', __name__, static_folder="../static")


@public.route("/")
def home():
    w = get_current_weather()
    current_temp = w.temp if w else None
    max_temp = get_max_temp_today()
    min_temp = get_min_temp_today()
    avg_temp = get_average_temp_today()

    kessel_data = get_kessel_current_data()
    puffer_data = get_puffer_current_data()
    lager_data = get_lager_current_data()

    pellets_today = get_pellets_consumption_today()
    pellets_last_week = get_pellets_consumption_last_n_days(6)

    pellets_kessel_stock = None
    pellets_total_consumption = None
    pellets_total_stock = None
    kessel_temp = None
    kessel_pressure = None
    kessel_feed_line_temp = None
    kessel_exhaust_temp = None
    kessel_exhaust_blower = None
    kessel_residual_oxygen = None
    kessel_usage_since_service = None
    kessel_usage_since_deashing = None
    kessel_usage_since_box_exhaustion = None
    operating_hours = None

    if kessel_data:
        pellets_total_consumption = kessel_data.pellets_total
        pellets_kessel_stock = kessel_data.reservoir_capacity
        kessel_temp = kessel_data.temperature
        kessel_pressure = kessel_data.pressure
        kessel_feed_line_temp = kessel_data.feed_line_temperature
        kessel_exhaust_temp = kessel_data.exhaust_temperature
        kessel_exhaust_blower = kessel_data.exhaust_blower
        kessel_residual_oxygen = kessel_data.residual_oxygen
        kessel_usage_since_service = kessel_data.usage_since_service
        if kessel_usage_since_service and kessel_usage_since_service > 0:
            kessel_usage_since_service = kessel_usage_since_service / 10
        kessel_usage_since_deashing = kessel_data.usage_since_deashing
        kessel_usage_since_box_exhaustion = kessel_data.usage_since_box_exhaustion
        operating_hours = kessel_data.operating_hours

    if lager_data:
        pellets_total_stock = lager_data.stock

    operating_hours_last_week = get_operating_hours_last_n_days()

    puffer_temperature_top = None
    puffer_temperature_bottom = None
    puffer_temp_water_storage = None

    if puffer_data:
        puffer_temperature_top = puffer_data.temperature_top
        puffer_temperature_bottom = puffer_data.temperature_bottom
        puffer_temp_water_storage = puffer_data.hot_water_storage_temp

    return render_template("public/home.html",
                            current_temp=current_temp, max_temp_today=max_temp,
                            min_temp_today=min_temp, avg_temp_today=avg_temp,
                            pellets_today=pellets_today, pellets_last_week=pellets_last_week,
                            pellets_kessel_stock=pellets_kessel_stock, pellets_total_consumption=pellets_total_consumption,
                            pellets_total_stock=pellets_total_stock,
                            operating_hours=operating_hours, operating_hours_last_week=operating_hours_last_week,
                            puffer_temperature_top=puffer_temperature_top, puffer_temperature_bottom=puffer_temperature_bottom,
                            puffer_temp_water_storage=puffer_temp_water_storage,
                            kessel_temp=kessel_temp, kessel_pressure=kessel_pressure,
                            kessel_feed_line_temp=kessel_feed_line_temp, kessel_exhaust_temp=kessel_exhaust_temp,
                            kessel_exhaust_blower=kessel_exhaust_blower, kessel_residual_oxygen=kessel_residual_oxygen,
                            kessel_usage_since_service=kessel_usage_since_service, kessel_usage_since_deashing=kessel_usage_since_deashing,
                            kessel_usage_since_box_exhaustion=kessel_usage_since_box_exhaustion)

@public.route("/about/")
def about():
    return render_template("public/about.html")

@public.route("/sitemap.xml")
def sitemap():
    pass
    # url_root = request.url_root[:-1]
    # pages = []
    # today = datetime.now()
    # ten_days_ago = (today - timedelta(days=10)).date().isoformat()
    # # static pages
    # for rule in current_app.url_map.iter_rules():
    #     if "GET" in rule.methods and len(rule.arguments) == 0:
    #         url = url_root + '%s' % rule.rule
    #         pages.append([url, ten_days_ago])

    # # daily charts
    # start_date = dateutil.parser.parse(get_first_date())
    # total_days = (today - start_date).days + 1

    # for day_number in range(total_days):
    #     current_date = (start_date + timedelta(days=day_number)).date()
    #     url = url_root + url_for('charts.daily') + '/%s' % current_date
    #     pages.append([url, current_date])

    # sitemap_xml = render_template("public/sitemap_template.xml", pages=pages)
    # response = make_response(sitemap_xml)
    # response.headers["Content-Type"] = "application/xml"

    # return response
