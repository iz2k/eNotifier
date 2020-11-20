from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy_utils import database_exists, create_database

from eNotifierBackend.dbManager import dbCredentials, myBase, Measurement, CityMeas, HomeMeas


class dbController:

    def __init__(self):
        SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://' + dbCredentials['user'] + ':' + dbCredentials['pass'] + '@' + \
                                  dbCredentials['host'] + '/' + dbCredentials['db']

        # Initialize DB handler
        if not database_exists(SQLALCHEMY_DATABASE_URI):
            print('DB missing. Creating new DB.')
            create_database(SQLALCHEMY_DATABASE_URI)

        self.engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=100)
        self.sessionmaker = sessionmaker(bind=self.engine)
        print('DB engine ready.')

        # Generate database schema with imported elements
        myBase.metadata.create_all(self.engine)

        #self.testRelationship()

    def insert(self, object):
        tStart = datetime.now()
        session = self.sessionmaker()
        session.add(object)
        session.commit()
        session.close()
        tStop = datetime.now()
        print('\t> Insert time: ' + str(tStop-tStart))

    def load(self, table):
        tStart = datetime.now()
        session = self.sessionmaker()
        result = session.query(table).options(selectinload('*'))

        session.close()
        tStop = datetime.now()
        print('\t> Load time: ' + str(tStop - tStart))
        return result

    def loadMeasurements(self, dStart, dStop):
        tStart = datetime.now()
        session = self.sessionmaker()
        result = session.query(Measurement).options(selectinload('*')).\
            filter(Measurement.datetime <= dStop).\
            filter(Measurement.datetime >= dStart)

        session.close()
        tStop = datetime.now()
        print('\t> Load time: ' + str(tStop - tStart))
        return result

    def testRelationship(self):
        print('Test Realtionship within DB:')
        # INSERT DATA
        myMeas = Measurement(
                    datetime=datetime.now(),
                    cityMeas = CityMeas(
                        location='San Sebastian',
                        temperature=18.7,
                        pressure=1001,
                        humidity=82.3,
                        uvi=82.3,
                        wind_speed=13.2,
                        wind_degree=21,
                        pop=0.45
                    ),
                    homeMeas = HomeMeas(
                        temperature=25.6,
                        pressure=1012,
                        humidity=82.3,
                        gas_resistance=40000,
                        eco2=1058,
                        tvoc=138
                    )
                )

        self.insert(myMeas)

        # LOAD DATA
        lastTest = self.load(Measurement).order_by(Measurement.id.desc()).first()
        print(lastTest)