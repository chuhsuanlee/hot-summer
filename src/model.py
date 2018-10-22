# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DailyRecord(Base):
    __tablename__ = 'daily_record'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    max_temperature = Column(Numeric(5, 2))
    min_temperature = Column(Numeric(5, 2))
