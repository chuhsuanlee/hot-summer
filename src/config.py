# -*- coding: utf-8 -*-

API_KEY = '********************************'
API_CALLS = 10  # maximum is 1000 due to the free amount of API calls

CITY_MAP = {
    0: ('Berlin', (52.517, 13.3899)),
    1: ('Boston', (42.3601, -71.0589)),
}

SQLALCHEMY_URI = '{driver}://{user}:{pwd}@{host}/{db}?charset=utf8' \
    .format(
        driver='mysql+pymysql',
        host='127.0.0.1:3306',
        user='root',
        pwd='0000',
        db='chuhsuanlee'
    )
SQLALCHEMY_ECHO = False
