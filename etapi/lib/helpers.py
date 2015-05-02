# -*- coding: utf-8 -*-
import calendar
from datetime import datetime

def get_todays_date():
    return datetime.now().date()

def get_timestamps(series):
    """
    Create a timestamp for every created_at date and set the seconds zero.
    """
    return [
        1000 * calendar.timegm(
            datetime.strptime(d.created_at.split(".")[0], "%Y-%m-%d %H:%M:%S")
            .replace(second=0).timetuple()) for d in series]
