# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import calendar

from flask import (Blueprint, request, render_template)

from etapi.lib.helpers import get_timestamps
from etapi.lib.helpers import get_todays_date
from etapi.kesseldata.helpers import get_pellets_consumption_for_day
from etapi.kesseldata.helpers import get_puffer_daily_series
from etapi.kesseldata.helpers import get_kessel_daily_series
from etapi.kesseldata.helpers import get_daily_pellets_consumption_last_7_days
from etapi.kesseldata.helpers import get_daily_operating_hours_last_7_days
from etapi.kesseldata.helpers import get_operating_hours_for_day


charts = Blueprint('charts', __name__, url_prefix='/charts',
                    static_folder="../static")

@charts.route("/daily")
@charts.route("/daily/<date>")
def daily(date=get_todays_date().strftime('%Y-%m-%d')):
    try:
        current_date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError, TypeError:
        current_date = get_todays_date()

    yesterday = current_date - timedelta(days=1)
    tomorrow = current_date + timedelta(days=1)

    kessel_data = get_kessel_daily_series(current_date)
    timestamps_kessel = get_timestamps(kessel_data)

    kessel_temp = [list(x) for x in zip(timestamps_kessel, [(int(d.temperature or 0)) for d in kessel_data])]
    kessel_pressure = [list(x) for x in zip(timestamps_kessel, [(float(d.pressure or 0)) for d in kessel_data])]
    kessel_feed_line_temperature  = [list(x) for x in zip(timestamps_kessel, [(int(d.feed_line_temperature or 0)) for d in kessel_data])]

    puffer_data = get_puffer_daily_series(current_date)
    timestamps_puffer = get_timestamps(puffer_data)

    puffer_temp_top_data = [list(x) for x in zip(timestamps_puffer, [(int(d.temperature_top or 0)) for d in puffer_data])]
    puffer_temp_bottom_data = [list(x) for x in zip(timestamps_puffer, [(int(d.temperature_bottom or 0)) for d in puffer_data])]
    puffer_temp_hot_water_storage = [list(x) for x in zip(timestamps_puffer, [(int(d.hot_water_storage_temp or 0)) for d in puffer_data])]

    pellets_usage_today = get_pellets_consumption_for_day(current_date)
    operating_hours = get_operating_hours_for_day(current_date)

    return render_template("charts/daily.html",
                            today=current_date, yesterday=yesterday, tomorrow=tomorrow,
                            puffer_temp_top_data=puffer_temp_top_data,
                            puffer_temp_bottom_data=puffer_temp_bottom_data,
                            puffer_temp_hot_water_storage=puffer_temp_hot_water_storage,
                            kessel_temp=kessel_temp,
                            kessel_pressure=kessel_pressure,
                            kessel_feed_line_temperature=kessel_feed_line_temperature,
                            pellets_usage_today=pellets_usage_today,
                            operating_hours=operating_hours)

@charts.route("/weekly")
def weekly():
    pellets_consumption = []
    operating_hours = []

    pellets_consumption_series = get_daily_pellets_consumption_last_7_days()
    operating_hours_series = get_daily_operating_hours_last_7_days()

    if not pellets_consumption_series and not operating_hours_series:
         return render_template("charts/weekly.html", no_data=True)

    # Calculate the timestamps
    timeseries_data = pellets_consumption_series if pellets_consumption_series else operating_hours_series
    timestamps = [1000 * calendar.timegm(datetime.strptime(d.created_at, '%Y-%m-%d').timetuple()) for d in timeseries_data]

    if pellets_consumption_series:
        pellets_consumption = [list(x) for x in zip(timestamps, [(int(d.pellets_consumption or 0)) for d in pellets_consumption_series])]
        total_pellets = sum(x.pellets_consumption for x in pellets_consumption_series)
    if operating_hours_series:
        operating_hours = [list(x) for x in zip(timestamps, [(int((d.operating_hours or 0) * 1000)) for d in operating_hours_series])]
        total_oh = sum(x.operating_hours for x in operating_hours_series)

    return render_template("charts/weekly.html",
                            pellets_consumption=pellets_consumption,
                            operating_hours=operating_hours,
                            total_pellets=total_pellets,
                            total_oh=total_oh)


@charts.route("/monthly")
def monthly():
    pass
