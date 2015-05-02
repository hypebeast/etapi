# -*- coding: utf-8 -*-
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)

from etapi.database import db
from etapi.weather.helpers import get_current_weather, get_max_temp_today, get_min_temp_today, get_average_temp_today
from etapi.kesseldata.helpers import get_pellets_consumption_today
from etapi.kesseldata.helpers import get_pellets_consumption_last_n_days
from etapi.kesseldata.helpers import get_pellets_total_consumption
from etapi.kesseldata.helpers import get_pellets_kessel_stock
from etapi.kesseldata.helpers import get_pellets_total_stock
from etapi.kesseldata.helpers import get_operating_hours_total
from etapi.kesseldata.helpers import get_operating_hours_last_n_days

public = Blueprint('public', __name__, static_folder="../static")


@public.route("/")
def home():
    w = get_current_weather()
    current_temp = w.temp if w else None
    max_temp = get_max_temp_today()
    min_temp = get_min_temp_today()
    avg_temp = get_average_temp_today()

    pellets_today = get_pellets_consumption_today()
    pellets_last_week = get_pellets_consumption_last_n_days(7)
    pellets_kessel_stock = get_pellets_kessel_stock()
    pellets_total_consumption = get_pellets_total_consumption()
    pellets_total_stock = get_pellets_total_stock()

    operating_hours = get_operating_hours_total()
    operating_hours_last_week = get_operating_hours_last_n_days()

    return render_template("public/home.html",
                            current_temp=current_temp, max_temp_today=max_temp,
                            min_temp_today=min_temp, avg_temp_today=avg_temp,
                            pellets_today=pellets_today, pellets_last_week=pellets_last_week,
                            pellets_kessel_stock=pellets_kessel_stock, pellets_total_consumption=pellets_total_consumption,
                            pellets_total_stock=pellets_total_stock,
                            operating_hours=operating_hours, operating_hours_last_week=operating_hours_last_week)

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
