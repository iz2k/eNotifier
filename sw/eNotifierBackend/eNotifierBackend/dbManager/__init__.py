from sqlalchemy.ext.declarative import declarative_base
myBase = declarative_base()

from eNotifierBackend.dbManager.dbModels import \
    Measurement, \
    HomeMeas, \
    CityMeas

dbCredentials = {
    'host': 'localhost',
    'user': 'pi',
    'pass': 'raspberry',
    'db': 'weather_station_db'
}
