# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from sqlalchemy import func

from etapi.lib.helpers import get_local_start_of_day_time, get_local_time, get_todays_date, get_start_of_day_in_utc_time
from etapi.kesseldata.models import Kessel, Lager, Puffer


def get_pellets_consumption_today():
    """
    Returns the pellets consumption for today.
    """
    start_date = get_local_start_of_day_time()
    end_date = start_date + timedelta(days=1)
    return Kessel.query.with_entities((func.max(Kessel.pellets_total) - func.min(Kessel.pellets_total)).label('pellets_consumption')).filter(
        Kessel.created_at >= start_date).filter(
        Kessel.created_at <= end_date).first().pellets_consumption

def get_pellets_consumption_for_day(d=datetime.now()):
    """
    Returns the pellets consumption for the specified day.
    """
    start_date = get_start_of_day_in_utc_time(d)
    end_date = start_date + timedelta(days=1)
    return Kessel.query.with_entities((func.max(Kessel.pellets_total) - func.min(Kessel.pellets_total)).label('pellets_consumption')).filter(
        Kessel.created_at >= start_date).filter(
        Kessel.created_at <= end_date).first().pellets_consumption

def get_pellets_consumption_last_n_days(n=7):
    """
    Returs the pellets consumption for the last n days. Today is included.
    """
    return Kessel.query.with_entities((func.max(Kessel.pellets_total) - func.min(Kessel.pellets_total)).label('pellets_consumption')).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) >= (datetime.utcnow() - timedelta(days=n))).first().pellets_consumption

def get_kessel_current_data():
    pass

def get_kessel_daily_series(current_date=datetime.utcnow()):
    tomorrow = current_date + timedelta(days=1)
    return Kessel.query.with_entities(Kessel.created_at, Kessel.temperature, Kessel.pressure, Kessel.feed_line_temperature).filter(
        Kessel.created_at >= current_date.strftime('%Y-%m-%d')).filter(
        Kessel.created_at < tomorrow.strftime('%Y-%m-%d')).all()

def get_puffer_daily_series(current_date=datetime.utcnow()):
    tomorrow = current_date + timedelta(days=1)
    return Puffer.query.with_entities(Puffer.created_at, Puffer.temperature_top,
                                        Puffer.temperature_bottom, Puffer.hot_water_storage_temp).filter(
        Puffer.created_at >= current_date.strftime('%Y-%m-%d')).filter(
        Puffer.created_at < tomorrow.strftime('%Y-%m-%d')).all()

def get_daily_pellets_consumption_last_7_days():
    """
    Returns an array with the daily pellets consumption for the last seven days.
    """
    today = datetime.utcnow()
    return Kessel.query.with_entities((func.max(Kessel.pellets_total) - func.min(Kessel.pellets_total)).label('pellets_consumption'),
                                            func.strftime('%Y-%m-%d', Kessel.created_at).label('created_at')).filter(
        Kessel.created_at >= (today - timedelta(days=7)).strftime('%Y-%m-%d')).filter(
        Kessel.created_at <= today.strftime('%Y-%m-%d')).group_by(func.strftime('%Y-%m-%d', Kessel.created_at)).all()


def get_daily_operating_hours_last_7_days():
    """
    Returns an array with the daily operating_hours for the last seven days.
    """
    today = datetime.utcnow()
    return Kessel.query.with_entities((func.max(Kessel.operating_hours) - func.min(Kessel.operating_hours)).label('operating_hours'),
                                            func.strftime('%Y-%m-%d', Kessel.created_at).label('created_at')).filter(
        Kessel.created_at >= (today - timedelta(days=7)).strftime('%Y-%m-%d')).filter(
        Kessel.created_at <= today.strftime('%Y-%m-%d')).group_by(func.strftime('%Y-%m-%d', Kessel.created_at)).all()


def get_pellets_total_consumption():
    """
    Returns the total pellets consumption.
    """
    result = Kessel.query.with_entities(Kessel.pellets_total).filter(
                func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
                Kessel.id.desc()).first()

    if not result:
        return None

    return result.pellets_total

def get_pellets_kessel_stock():
    """
    Returns the kessel pellets stock.
    """
    result = Kessel.query.with_entities(Kessel.reservoir_capacity).filter(
                func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
                Kessel.id.desc()).first()

    if not result:
        return None

    return result.reservoir_capacity

def get_pellets_total_stock():
    """
    Returns the total pellets stock.
    """
    result = Lager.query.with_entities(Lager.stock).filter(
                func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
                Lager.id.desc()).first()

    if not result:
        return None

    return result.stock

def get_operating_hours_total():
    """
    Returns the total operating hours.
    """
    result = Kessel.query.with_entities(Kessel.operating_hours).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Kessel.id.desc()).first()

    if not result:
        return None

    return result.operating_hours

def get_operating_hours_last_n_days(n=7):
    """
    Returns the operating hours for the last n days.
    """
    result = Kessel.query.with_entities((func.max(Kessel.operating_hours) - func.min(Kessel.operating_hours)).label('operating_hours')).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) > (datetime.utcnow() - timedelta(days=n))).first()

    if not result:
        return None

    return result.operating_hours

def get_kessel_current_temp():
    result = Kessel.query.with_entities(Kessel.temperature).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Kessel.id.desc()).first()

    if not result:
        return None

    return result.temperature

def get_kessel_current_pressure():
    result = Kessel.query.with_entities(Kessel.pressure).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Kessel.id.desc()).first()

    if not result:
        return None

    return result.pressure

def get_kessel_current_feed_line_temp():
    result = Kessel.query.with_entities(Kessel.feed_line_temperature).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Kessel.id.desc()).first()

    if not result:
        return None

    return result.feed_line_temperature

def get_kessel_current_exhaust_temp():
    result = Kessel.query.with_entities(Kessel.exhaust_temperature).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Kessel.id.desc()).first()

    if not result:
        return None

    return result.exhaust_temperature

def get_kessel_current_exhaust_blower():
    result = Kessel.query.with_entities(Kessel.exhaust_blower).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Kessel.id.desc()).first()

    if not result:
        return None

    return result.exhaust_blower

def get_kessel_current_residual_oxygen():
    result = Kessel.query.with_entities(Kessel.residual_oxygen).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Kessel.id.desc()).first()

    if not result:
        return None

    return result.residual_oxygen

def get_kessel_usage_since_service():
    result = Kessel.query.with_entities(Kessel.usage_since_service).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Kessel.id.desc()).first()

    if not result:
        return None

    return result.usage_since_service

def get_kessel_usage_since_deashing():
    result = Kessel.query.with_entities(Kessel.usage_since_deashing).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Kessel.id.desc()).first()

    if not result:
        return None

    return result.usage_since_deashing

def get_kessel_usage_since_box_exhaustion():
    result = Kessel.query.with_entities(Kessel.usage_since_box_exhaustion).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Kessel.id.desc()).first()

    if not result:
        return None

    return result.usage_since_box_exhaustion

def get_puffer_temperature_top():
    """
    Returns the current top puffer temperature.
    """
    result = Puffer.query.with_entities(Puffer.temperature_top).filter(
        func.strftime('%Y-%m-%d', Puffer.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Puffer.id.desc()).first()

    if not result:
        return None

    return result.temperature_top


def get_puffer_temperature_bottom():
    """
    Returns the current top puffer temperature.
    """
    result = Puffer.query.with_entities(Puffer.temperature_bottom).filter(
        func.strftime('%Y-%m-%d', Puffer.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Puffer.id.desc()).first()

    if not result:
        return None

    return result.temperature_bottom

def get_puffer_current_temp_water_storage():
    result = Puffer.query.with_entities(Puffer.hot_water_storage_temp).filter(
        func.strftime('%Y-%m-%d', Puffer.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Puffer.id.desc()).first()

    if not result:
        return None

    return result.hot_water_storage_temp
