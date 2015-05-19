# -*- coding: utf-8 -*-
import calendar
from datetime import datetime
import pytz

import tzlocal


def get_todays_date():
    """
    Returns the todays datetime.
    """
    return datetime.now()

def get_current_week_number():
    """
    Returns the current week number.
    """
    return get_week_number()

def get_week_number(dt=datetime.now()):
    """
    Returns the week number for the given date.
    """
    return dt.date().isocalendar()[1]

def get_timestamps(series):
    """
    Create a timestamp for every created_at date and set the seconds zero.
    """
    return [1000 * calendar.timegm(d.created_at.replace(second=0).timetuple()) for d in series]

def get_start_of_today_in_utc_time():
    """
    Returns the local start time of today in UTC time.
    """
    dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return dt - get_utc_offset()

def get_start_of_day_in_utc_time(dt=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)):
    """
    """
    # Start of day in local time
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
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
