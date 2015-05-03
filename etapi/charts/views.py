# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from flask import (Blueprint, request, render_template)

from etapi.lib.helpers import get_timestamps
from etapi.lib.helpers import get_todays_date
from etapi.kesseldata.helpers import get_pellets_consumption_for_day
from etapi.kesseldata.helpers import get_puffer_daily_series
from etapi.kesseldata.helpers import get_kessel_daily_series


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
    kessel_pressure = [list(x) for x in zip(timestamps_kessel, [(int(d.pressure or 0)) for d in kessel_data])]
    kessel_feed_line_temperature  = [list(x) for x in zip(timestamps_kessel, [(int(d.feed_line_temperature or 0)) for d in kessel_data])]

    puffer_data = get_puffer_daily_series(current_date)
    timestamps_puffer = get_timestamps(puffer_data)

    puffer_temp_top_data = [list(x) for x in zip(timestamps_puffer, [(int(d.temperature_top or 0)) for d in puffer_data])]
    puffer_temp_bottom_data = [list(x) for x in zip(timestamps_puffer, [(int(d.temperature_bottom or 0)) for d in puffer_data])]
    puffer_temp_hot_water_storage = [list(x) for x in zip(timestamps_puffer, [(int(d.hot_water_storage_temp or 0)) for d in puffer_data])]

    pellets_usage_today = get_pellets_consumption_for_day(current_date)

    return render_template("charts/daily.html",
                            today=current_date, yesterday=yesterday, tomorrow=tomorrow,
                            puffer_temp_top_data=puffer_temp_top_data,
                            puffer_temp_bottom_data=puffer_temp_bottom_data,
                            puffer_temp_hot_water_storage=puffer_temp_hot_water_storage,
                            kessel_temp=kessel_temp,
                            kessel_pressure=kessel_pressure,
                            kessel_feed_line_temperature=kessel_feed_line_temperature,
                            pellets_usage_today=pellets_usage_today)
