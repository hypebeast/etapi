# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from flask import (Blueprint, request, render_template, redirect, url_for)

from etapi.lib.helpers import get_timestamps
from etapi.lib.helpers import get_todays_date
from etapi.lib.helpers import convert_series_to_local_time
from etapi.weather.helpers import get_daily_temperature_series


weather = Blueprint('weather', __name__, url_prefix='/weather',
                    static_folder="../static")


@weather.route("/")
@weather.route("/<date>")
def index(date=None):
    if not date:
        date = get_todays_date().strftime('%Y-%m-%d')

    try:
        current_date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError, TypeError:
        current_date = get_todays_date()

    yesterday = current_date - timedelta(days=1)
    tomorrow = current_date + timedelta(days=1)

    temp_data = get_daily_temperature_series(current_date)

    print temp_data

    timestamps_temp = get_timestamps(temp_data)

    daily_chart_data = [list(x) for x in zip(timestamps_temp, [(float(d.temp or 0 )) for d in temp_data])]
    daily_chart_data = convert_series_to_local_time(daily_chart_data)

    return render_template("weather/weather.html",
                            today=current_date, yesterday=yesterday, tomorrow=tomorrow,
                            data=daily_chart_data)
