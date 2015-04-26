# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from sqlalchemy import func

from etapi.kesseldata.models import Kessel


def get_pellets_usage_today():
    """
    Returns the pellets usage for today
    """
    return Kessel.query.with_entities((func.max(Kessel.pellets_total)- func.min(Kessel.pellets_total)).label('todays_usage')).filter(
        func.strftime('%Y-%m-%d', Kessel.created_at) == datetime.utcnow().strftime('%Y-%m-%d')).first().todays_usage

def get_pellets_usage_last_n_days():
    pass

def get_pellets_total_stock():
    pass

def get_pellets_kessel_stock():
    pass

