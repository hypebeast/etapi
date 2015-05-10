# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from sqlalchemy import func

from etapi.lib.helpers import get_local_start_of_day_time, get_local_time, get_todays_date
from etapi.weather.models import Weather


def get_current_weather():
    """
    returns the lates entry from the weather table
    """
    return Weather.query.with_entities(Weather.temp).filter(
        Weather.created_at >= (datetime.now() - timedelta(days=2))).order_by(
        Weather.id.desc()).first()

def get_max_temp_today():
    """
    Returns the maximum temperature for today.
    """
    start_date = get_local_start_of_day_time()
    end_date = start_date + timedelta(days=1)
    print end_date
    return Weather.query.with_entities(func.max(Weather.temp).label("temp_max")).filter(
            Weather.created_at >= start_date).filter(
            Weather.created_at <= end_date).first().temp_max

def get_min_temp_today():
    """
    Returns the minimum temperature for today.
    """
    start_date = get_local_start_of_day_time()
    end_date = start_date + timedelta(days=1)
    return Weather.query.with_entities(func.min(Weather.temp).label("temp_min")).filter(
            Weather.created_at >= start_date).filter(
            Weather.created_at <= end_date).first().temp_min

def get_average_temp_today():
    """
    Returns the average temperature for today.
    """
    start_date = get_local_start_of_day_time()
    end_date = start_date + timedelta(days=1)
    return Weather.query.with_entities(func.avg(Weather.temp).label("temp_avg")).filter(
            Weather.created_at >= start_date).filter(
            Weather.created_at <= end_date).first().temp_avg

def get_daily_temperature_series(current_date=get_todays_date().strftime('%Y-%m-%d')):
    start_date = get_local_time(current_date)
    end_date = start_date + timedelta(days=1)
    return Weather.query.with_entities(Weather.created_at, Weather.temp).filter(
        Weather.created_at >= start_date).filter(
        Weather.created_at < end_date).all()
