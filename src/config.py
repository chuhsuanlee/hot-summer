# -*- coding: utf-8 -*-

API_KEY = '********************************'
API_CALLS = 5  # maximum is 1000 due to the free amount of API calls

CITY_MAP = {
    0: ('Berlin', (52.517, 13.3899)),
}

SQLALCHEMY_URI = '{driver}://{user}:{pwd}@{host}/{db}?charset=utf8' \
    .format(
        driver='mysql+pymysql',
        host='10.0.2.15:3306',
        user='root',
        pwd='0000',
        db='default'
    )
SQLALCHEMY_ECHO = False
