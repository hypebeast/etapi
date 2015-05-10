# -*- coding: utf-8 -*-
import calendar
from datetime import datetime
import pytz

import tzlocal


def get_todays_date():
    return datetime.now().date()

def get_timestamps(series):
    """
    Create a timestamp for every created_at date and set the seconds zero.
    """
    return [1000 * calendar.timegm(d.created_at.replace(second=0).timetuple()) for d in series]

def get_local_start_of_day_time():
    dt = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    return dt - get_utc_offset()

def get_local_time(dt=datetime.utcnow()):
    return dt - get_utc_offset()

def get_utc_offset():
    dt = datetime.now()
    local_tz = tzlocal.get_localzone()
    tz = pytz.timezone(local_tz.__str__())
    return tz.utcoffset(dt)

def convert_series_to_local_time(series):
    offset = get_utc_offset().total_seconds() * 1000
    timestamps = [x[0] + offset for x in series]
    return zip(timestamps, [x[1] for x in series])
