# Document

This project uses [Dark Sky](https://darksky.net/) API wrapped by [python-forecastio](https://pypi.org/project/python-forecastio/) as a tool to have a quick look on the historical weather data and derive some insights from it.

## Requirements

* Since this project is [dockerized](Dockerfile), [Docker](https://docs.docker.com/install/) needs to be installed to run this project.

* An API key must be claimed beforehand. Please go to [this page](https://darksky.net/dev) and claim yours.

## Quick start

After cloning this repository to your local machine, substitute the **API_KEY** in [config.py](src/config.py) with the key retrieved from above.

There are some commands you can use as indicated in [Makefile](Makefile), or simply type `make help`, it will show the Make commands that can be used.

More variables in [config.py](src/config.py):

* **API_CALLS**: How many API calls available

* **CITY_MAP**: Dictionary that the city list is set as. Berlin is in default, and more cities can be added as an item with the format of `incremental_int: (‘city_name’, (latitude, longitude))` as follows:
  ```py
  CITY_MAP = {
      0: ('Berlin', (52.517, 13.3899)),
      1: ('Boston', (42.3601, -71.0589)),
  }
  ```

* **SQLALCHEMY_URI**, **SQLALCHEMY_ECHO**: The configuration of database. It uses [PyMySQL](https://pypi.org/project/PyMySQL/) and [SQLAlchemy](https://pypi.org/project/SQLAlchemy/) packages as the communication tool between the program and database.

## Functions

[download_historical_data()](src/main.py#L15) fetches the historical daily data and saves a [csv file](src/reports/Berlin_report_sample.csv) in reports folder.

For historical data, only one day per API call can be fetched, and that’s the reason why the amount of API calls should be set beforehand in [config.py](src/config.py). The process begins from yesterday, then one day before, and continues this way until it reaches the maximum of possible API calls.

The record model table schema is specified in [model.py](src/model.py) and database is configured in [config.py](src/config.py). Related operations include [update_record()](src/tools.py#L27) and [update_process()](src/main.py#L73).

Since there’s no real database server binded yet, this project uses the [csv file](src/reports/Berlin_report_sample.csv) as depicted above to retrieve the information.

[daily_update()](src/main.py#L62) is the function excluded from execution but implemented as a procedure that keeps this database automatically updated for a set of cities. It assumes that after [download_historical_data()](src/main.py#L15), data before yesterday are all downloaded, so only data of yesterday (when the date moves to the next day, there’s no data for the ‘new’ yesterday yet) and forecasted data of the following 7 days need to be fetched or updated. Thus, it uses the [Time Machine Request](https://darksky.net/dev/docs#time-machine-request) and [Forecast Request](https://darksky.net/dev/docs#forecast-request) separately.

[required_computation()](src/main.py#L100) reads the [csv file](src/reports/Berlin_report_sample.csv) saved in [download_historical_data()](src/main.py#L15). It compares the maximum temperature of every single day in summer (June - August) between 2016-2018, and calculates the amount of hottest days in each year.

## Sample output
```
Berlin historical record on 2018-10-21: 15/5.56
Berlin historical record on 2018-10-20: 12.44/2.56
Berlin historical record on 2018-10-19: 14.44/2.44
Berlin historical record on 2018-10-18: 15.75/7.44
Berlin historical record on 2018-10-17: 20.57/6

Successfully read 900 daily data.

The amount of hottest days in summer (June - August) between 2016 - 2018:
2016 has 21 hottest days.
2017 has 22 hottest days.
2018 has 49 hottest days.

Result report: The hottest year is 2018 with 49 hottest days in summer.
```
