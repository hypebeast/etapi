# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from etapi.extensions import db
from etapi.lib.helpers import get_start_of_day_in_utc_time, get_todays_date


def get_table_data(today=None):
    if not today:
        today = get_todays_date()

    start_date = get_start_of_day_in_utc_time(today)
    last_30_days = today - timedelta(days=30)

    data = db.engine.execute(
        "SELECT "
            "k.*, w.max_temp, w.min_temp, w.avg_temp, l.pellets_stock "
        "FROM ("
            "SELECT "
                "strftime('%Y-%m-%d', created_at) AS created_at, "
                "max(pellets_total) - min(pellets_total) AS pellets_usage, "
                "max(pellets_total) AS pellets_total, "
                "max(operating_hours) - min(operating_hours) AS operating_hours "
            "FROM kessel_data "
            "WHERE created_at > ? "
            "GROUP BY strftime('%Y-%m-%d', created_at)) k "
        "JOIN ("
            "SELECT "
                "strftime('%Y-%m-%d', created_at) AS created_at, "
                "max(temp) AS max_temp, "
                "min(temp) AS min_temp, "
                "avg(temp) AS avg_temp "
            "FROM weather_data "
            "WHERE created_at > ? "
            "GROUP BY strftime('%Y-%m-%d', created_at)"
        ") w ON k.created_at = w.created_at "
        "JOIN ("
            "SELECT "
                "strftime('%Y-%m-%d', created_at) AS created_at, "
                "min(stock) AS pellets_stock "
            "FROM lager_data "
            "WHERE created_at > ? "
            "GROUP BY strftime('%Y-%m-%d', created_at)"
        ") l ON k.created_at = l.created_at "
        "ORDER BY created_at DESC",
        (last_30_days, last_30_days, last_30_days))

    return list(data)
