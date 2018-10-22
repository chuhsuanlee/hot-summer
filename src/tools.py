# -*- coding: utf-8 -*-

import codecs
import csv

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


def unicode_csv_dictreader(path, *args, **kwargs):
    """Create a csv dict reader that copes with encoding correctly."""
    # utf-8-sig strips off a BOM if it's present
    stream = codecs.open(path, encoding='utf-8-sig')
    return UnicodeCSVDictReader(stream, *args, **kwargs)


class UnicodeCSVDictReader(csv.DictReader):
    def __init__(self, unicode_csvfile, *args, **kwargs):
        decoder = codecs.getdecoder('utf-8')
        self.decoder = lambda v: decoder(v)[0]
        utf8_csvfile = codecs.iterencode(unicode_csvfile, encoding='utf-8')
        # bollicks to csv.DictReader being an oldstyle class
        csv.DictReader.__init__(self, utf8_csvfile, *args, **kwargs)
        self.fieldnames = [self.decoder(f) for f in self.fieldnames]

    def next(self):
        data = csv.DictReader.next(self)
        return {k: self.decoder(v) for (k, v) in data.iteritems()}
