# -*- coding: utf-8 -*-
import datetime as dt

from etapi.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)


class Kessel(SurrogatePK, Model):
    __tablename__ = 'kessel_data'

    id = Column(db.Integer(), nullable=False, primary_key=True)
    created_at = Column(db.DateTime(), nullable=False, default=dt.datetime.utcnow)
    operating_hours = Column(db.Integer(), nullable=True)
    pellets_stock = Column(db.Integer(), nullable=True)
    pellets_total = Column(db.Integer(), nullable=True)
    usage_since_service = Column(db.Integer(), nullable=True)
    reservoir_capacity = Column(db.Integer(), nullable=True)
    usage_since_deashing = Column(db.Integer(), nullable=True)
    usage_since_box_exhaustion = Column(db.Integer(), nullable=True)
    pressure = Column(db.Float(), nullable=True)
    temperature = Column(db.Integer(), nullable=True)
    feed_line_temperature = Column(db.Integer(), nullable=True)
    exhaust_temperature = Column(db.Integer(), nullable=True)
    exhaust_blower = Column(db.Integer(), nullable=True)
    residual_oxygen = Column(db.Float(), nullable=True)


class Puffer(SurrogatePK, Model):
    __tablename__ = 'puffer_data'

    id = Column(db.Integer(), nullable=False, primary_key=True)
    created_at = Column(db.DateTime(), nullable=False, default=dt.datetime.utcnow)
    temperature_top = Column(db.Integer(), nullable=True)
    temperature_bottom = Column(db.Integer(), nullable=True)
    hot_water_storage_temp = Column(db.Integer(), nullable=True)


class Lager(SurrogatePK, Model):
    __tablename__ = 'lager_data'

    id = Column(db.Integer(), nullable=False, primary_key=True)
    created_at = Column(db.DateTime(), nullable=False, default=dt.datetime.utcnow)
    stock = Column(db.Integer, nullable=True)


def __init__(self):
    db.Model.__init__(self)

