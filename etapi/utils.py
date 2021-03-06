# -*- coding: utf-8 -*-
'''Helper utilities and decorators.'''
import time

from flask import flash

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                    .format(getattr(form, field).label.text, error), category)

def pretty_date(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    Ref: https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
    """

    if default is None:
        default = 'just now'

    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if period == 1:
            return u'%d %s ago' % (period, singular)
        else:
            return u'%d %s ago' % (period, plural)

    return default

def pretty_seconds_to_hhmmss(seconds):
    if not seconds:
        return None
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d h %d m %s s" % (h, m, s)

def pretty_seconds_to_hhmm(seconds):
    if not seconds:
        return None
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d h %d m" % (h, m)

def pretty_seconds_to_hh(seconds):
    if not seconds:
        return None
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d h" % (h)
