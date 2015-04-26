# -*- coding: utf-8 -*-
import datetime as dt

from etapi.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)


class Weather(SurrogatePK, Model):
    __tablename__ = 'weather_data'

    id = Column(db.Integer(), nullable=False, primary_key=True)
    created_at = Column(db.Text(), nullable=False, default=dt.datetime.utcnow)
    temp = Column(db.Float(), nullable=True)


def __init__(self):
    db.Model.__init__(self)

