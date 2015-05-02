# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from sqlalchemy import func

from etapi.kesseldata.models import Kessel, Lager


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
    return Kessel.query.with_entities(Kessel.pellets_stock).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Kessel.id.desc()).first().pellets_stock

def get_pellets_total_stock():
    """
    Returns the total pellets stock.
    """
    return Lager.query.with_entities(Lager.stock).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Lager.id.desc()).first().stock

def get_operating_hours_total():
    """
    Returns the total operating hours.
    """
    return Kessel.query.with_entities(Kessel.operating_hours).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).order_by(
        Kessel.id.desc()).first().operating_hours

def get_operating_hours_last_n_days(n=7):
    """
    Returns the operating hours for the last n days.
    """
    return Kessel.query.with_entities((func.max(Kessel.operating_hours) - func.min(Kessel.operating_hours)).label('operating_hours')).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) > (datetime.utcnow() - timedelta(days=n))).first().operating_hours


