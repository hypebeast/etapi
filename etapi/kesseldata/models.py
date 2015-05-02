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


class Lager(SurrogatePK, Model):
    __tablename__ = 'lager_data'

    id = Column(db.Integer(), nullable=False, primary_key=True)
    created_at = Column(db.DateTime(), nullable=False, default=dt.datetime.utcnow)
    stock = Column(db.Integer, nullable=True)


def __init__(self):
    db.Model.__init__(self)

