# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import Pool, QueuePool

from config import SQLALCHEMY_URI, SQLALCHEMY_ECHO


# set default timezone to +00:00 => make sure to get a utc datetime object
@event.listens_for(Pool, "checkout")
def set_timezone(dbapi_connection, connectidon_record, connection_proxy):
    cursor = dbapi_connection.cursor()
    cursor.execute('SET @@session.time_zone = "+00:00";')


# prepare session
engine = create_engine(SQLALCHEMY_URI, poolclass=QueuePool, echo=SQLALCHEMY_ECHO)
Session = sessionmaker(bind=engine)
session = Session()


def update_record(src, tar):
    for k in tar.__table__.columns.keys():
        if k not in ['id'] and getattr(src, k) is not None:
            setattr(tar, k, getattr(src, k))
