# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from sqlalchemy import func

from etapi.kesseldata.models import Kessel, Lager, Puffer


def get_pellets_consumption_today():
    """
    Returns the pellets consumption for today.
    """
    return Kessel.query.with_entities((func.max(Kessel.pellets_total) - func.min(Kessel.pellets_total)).label('pellets_consumption')).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).first().pellets_consumption

def get_pellets_consumption_last_n_days(n=7):
    """
    Returs the pellets consumption for the last n days. Today is included.
    """
    return Kessel.query.with_entities((func.max(Kessel.pellets_total) - func.min(Kessel.pellets_total)).label('pellets_consumption')).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) > (datetime.utcnow() - timedelta(days=n))).first().pellets_consumption

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
