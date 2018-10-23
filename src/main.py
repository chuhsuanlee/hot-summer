# -*- coding: utf-8 -*-
import os
import traceback
from datetime import datetime, timedelta

from forecastio import load_forecast as forecast
from pandas import DataFrame

from config import API_KEY, API_CALLS, CITY_MAP
from model import DailyRecord
from tools import unicode_csv_dictreader
from tools import session, update_record


def download_historical_data():
    """Download the historical daily data as a csv file."""
    city_count = len(CITY_MAP)
    tracked_period = API_CALLS // city_count

    for city_index in xrange(city_count):
        report = DataFrame()
        tracking_day = datetime.utcnow()

        for i in xrange(tracked_period):
            tracking_day -= timedelta(days=1)
            this_city = forecast(API_KEY, *CITY_MAP[city_index][1], time=tracking_day, units='si')
            daily_record = this_city.daily().data[0]

            record = DailyRecord(
                city_id=city_index,
                year=tracking_day.year,
                month=tracking_day.month,
                day=tracking_day.day,
                max_temperature=daily_record.temperatureHigh,
                min_temperature=daily_record.temperatureLow,
            )
            session.add(record)
            session.commit()

            to_be_inserted = {
                'city_id': [record.city_id],
                'year': [record.year],
                'month': [record.month],
                'day': [record.day],
                'max_temperature': [record.max_temperature],
                'min_temperature': [record.min_temperature]
            }
            report = report.append(DataFrame(to_be_inserted))

            print '{} historical record on {}: {}/{}'.format(
                CITY_MAP[city_index][0],
                tracking_day.date(),
                record.max_temperature,
                record.min_temperature
            )

        os.chdir('/usr/src/app/reports')
        report.to_csv('{}_report.csv'.format(CITY_MAP[city_index][0]), encoding='utf-8',
                      columns=['city_id', 'year', 'month', 'day', 'max_temperature', 'min_temperature'])


def daily_update():
    """Update the data of yesterday and forecasted data of the following 7 days."""
    for city_index in xrange(len(CITY_MAP)):
        yesterday = datetime.utcnow() - timedelta(days=1)
        this_city = forecast(API_KEY, *CITY_MAP[city_index][1], time=yesterday, units='si')
        update_process(this_city, city_index)

        this_city = forecast(API_KEY, *CITY_MAP[city_index][1], units='si')
        update_process(this_city, city_index)


def update_process(forecast_object, city_index):
    """Update the existed record or add new record."""
    daily_records = forecast_object.daily().data
    for each_record in daily_records:
        tracking_day = each_record.time
        record = DailyRecord(
            city_id=city_index,
            year=tracking_day.year,
            month=tracking_day.month,
            day=tracking_day.day,
            max_temperature=each_record.temperatureHigh,
            min_temperature=each_record.temperatureLow,
        )
        record_matched = session.query(DailyRecord) \
                                .filter(DailyRecord.city_id == record.city_id) \
                                .filter(DailyRecord.year == record.year) \
                                .filter(DailyRecord.month == record.month) \
                                .filter(DailyRecord.day == record.day) \
                                .first()
        if record_matched:
            update_record(record, record_matched)
            session.commit()
        else:
            session.add(record)
            session.commit()


def required_computation():
    """Compare the weather of each day in summer (June - August) between 2016-2018."""
    os.chdir('/usr/src/app/reports')
    # read with csv reader (handle bom and unicode)
    try:
        read_data = list(unicode_csv_dictreader('Berlin_report_sample.csv'))
        print '\nSuccessfully read {} daily data.'.format(len(read_data))
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print '\nFailed to read data: {}'.format(traceback.format_exc())
        read_data = []

    highest_record_year = dict()
    year_statistics = {
        2016: 0,
        2017: 0,
        2018: 0,
    }

    for data in read_data:
        year = int(data['year'])
        month = int(data['month'])
        day = int(data['day'])
        max_temperature = float(data['max_temperature'])
        if month in (6, 7, 8):
            if (month, day) in highest_record_year:
                if highest_record_year[(month, day)][0] > max_temperature:
                    continue
            highest_record_year[(month, day)] = (max_temperature, year)

    for temp, max_year in highest_record_year.itervalues():
        year_statistics[max_year] += 1

    hottest_year = None
    hottest_days_count = 0
    print '\nThe amount of hottest days in summer (June - August) between 2016 - 2018:'
    for year, count in year_statistics.iteritems():
        print year, 'has', count, 'hottest days.'
        if hottest_days_count == 0 or count > hottest_days_count:
            hottest_year = year
            hottest_days_count = count

    print '\nResult report: The hottest year is {} with {} hottest days in summer.'.format(hottest_year, hottest_days_count)


if __name__ == "__main__":
    download_historical_data()
    daily_update()
    required_computation()
