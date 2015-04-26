# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from sqlalchemy import func

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
    today = datetime.utcnow()
    tomorrow = today + timedelta(days=1)
    return Weather.query.with_entities(func.max(Weather.temp).label("temp_max")).filter(
            Weather.created_at > today.strftime('%Y-%m-%d')).filter(
            Weather.created_at < tomorrow.strftime('%Y-%m-%d')).first().temp_max

def get_min_temp_today():
    """
    Returns the minimum temperature for today.
    """
    today = datetime.utcnow()
    tomorrow = today + timedelta(days=1)
    return Weather.query.with_entities(func.min(Weather.temp).label("temp_min")).filter(
            Weather.created_at > today.strftime('%Y-%m-%d')).filter(
            Weather.created_at < tomorrow.strftime('%Y-%m-%d')).first().temp_min

def get_average_temp_today():
    """
    Returns the average temperature for today.
    """
    return Weather.query.with_entities(func.avg(Weather.temp).label("temp_avg")).filter(
            func.strftime('%Y-%m-%d', Weather.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).first().temp_avg
