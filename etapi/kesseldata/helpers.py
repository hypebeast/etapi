# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from sqlalchemy import func

from etapi.lib.helpers import get_start_of_today_in_utc_time, get_todays_date, get_start_of_day_in_utc_time
from etapi.kesseldata.models import Kessel, Lager, Puffer


def get_pellets_consumption_for_day(d=datetime.now()):
    """
    Returns the pellets consumption for the specified day. By default the data
    for today is returned.
    """
    start_date = get_start_of_day_in_utc_time(d)
    end_date = start_date + timedelta(days=1)
    return Kessel.query.with_entities((func.max(Kessel.pellets_total) - func.min(Kessel.pellets_total)).label('pellets_consumption')).filter(
        Kessel.created_at >= start_date).filter(
        Kessel.created_at <= end_date).first().pellets_consumption

def get_pellets_consumption_today():
    """
    Returns the pellets consumption for today.
    """
    return get_pellets_consumption_for_day()

def get_pellets_consumption_last_n_days(n=7):
    """
    Returs the pellets consumption for the last n days. Today is included.
    """
    end_date = (datetime.utcnow() - timedelta(days=n)).strftime('%Y-%m-%d')
    return Kessel.query.with_entities((func.max(Kessel.pellets_total) - func.min(Kessel.pellets_total)).label('pellets_consumption')).filter(
        Kessel.created_at >= end_date).first().pellets_consumption

def get_daily_pellets_consumption_last_7_days():
    """
    Returns an array with the daily pellets consumption for the last seven days.
    """
    end_date = datetime.utcnow()
    start_date = (end_date - timedelta(days=6)).strftime('%Y-%m-%d')
    return Kessel.query.with_entities((func.max(Kessel.pellets_total) - func.min(Kessel.pellets_total)).label('pellets_consumption'),
                                            func.strftime('%Y-%m-%d', Kessel.created_at).label('created_at')).filter(
        Kessel.created_at >= start_date).filter(
        Kessel.created_at <= end_date).group_by(func.strftime('%Y-%m-%d', Kessel.created_at)).all()

def get_kessel_daily_series(dt=datetime.now()):
    """
    Returns the kessel data for the specified day. By default the data for
    today is returned.
    """
    start_date = get_start_of_day_in_utc_time(dt)
    end_date = start_date + timedelta(days=1)
    return Kessel.query.with_entities(Kessel.created_at,
                                        Kessel.temperature,
                                        Kessel.pressure,
                                        Kessel.feed_line_temperature).filter(
        Kessel.created_at >= start_date).filter(
        Kessel.created_at <= end_date).all()

def get_puffer_daily_series(dt=datetime.utcnow()):
    """
    Returns the puffer data for the specified day. By default the data for today
    is returned.
    """
    start_date = get_start_of_day_in_utc_time(dt)
    end_date = start_date + timedelta(days=1)
    return Puffer.query.with_entities(Puffer.created_at,
                                        Puffer.temperature_top,
                                        Puffer.temperature_bottom,
                                        Puffer.hot_water_storage_temp).filter(
        Puffer.created_at >= start_date).filter(
        Puffer.created_at <= end_date).all()

def get_operating_hours_for_day(dt=datetime.now()):
    """
    Returns the total operating hours for the given date.
    """
    start_date = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(hours=24)
    result = Kessel.query.with_entities((func.max(Kessel.operating_hours) - func.min(Kessel.operating_hours)).label('operating_hours')).filter(
        Kessel.created_at >= start_date).filter(
        Kessel.created_at < end_date).first().operating_hours

    if not result:
        return None

    return result

def get_daily_operating_hours_last_7_days():
    """
    Returns an array with the daily operating_hours for the last seven days.
    """
    end_date = datetime.utcnow()
    start_date = (end_date - timedelta(days=6)).strftime('%Y-%m-%d')
    return Kessel.query.with_entities((func.max(Kessel.operating_hours) - func.min(Kessel.operating_hours)).label('operating_hours'),
                                            func.strftime('%Y-%m-%d', Kessel.created_at).label('created_at')).filter(
        Kessel.created_at >= start_date).filter(
        Kessel.created_at <= end_date).group_by(func.strftime('%Y-%m-%d', Kessel.created_at)).all()

def get_operating_hours_last_n_days(n=6):
    """
    Returns the total operating hours for the last n days.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=n)
    result = Kessel.query.with_entities((func.max(Kessel.operating_hours) - func.min(Kessel.operating_hours)).label('operating_hours')).filter(
        Kessel.created_at >= start_date).filter(
        Kessel.created_at <= end_date).first()

    if not result:
        return None

    return result.operating_hours

def get_kessel_current_data():
    """
    Returns the current kessel data.
    """
    return Kessel.query.order_by(Kessel.id.desc()).first()

def get_puffer_current_data():
    """
    Returns the current puffer data.
    """
    return Puffer.query.order_by(Puffer.id.desc()).first()

def get_lager_current_data():
    """
    Returns the current lager data.
    """
    return Lager.query.order_by(Lager.id.desc()).first()
