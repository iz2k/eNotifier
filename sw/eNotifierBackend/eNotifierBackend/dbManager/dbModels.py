from sqlalchemy import Column, BigInteger, String, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from eNotifierBackend.dbManager import myBase
from eNotifierBackend.tools.jsonTools import prettyJson


class Measurement(myBase):
    __tablename__ = 'measurement'

    id = Column(BigInteger, primary_key=True)
    datetime = Column(DateTime)
    cityMeas = relationship("CityMeas", uselist=False, back_populates="measurement")
    homeMeas = relationship("HomeMeas", uselist=False, back_populates="measurement")

    def populate(self, arg):
        if type(arg) is dict:
            mydict = arg
        else:
            mydict = arg.__dict__

        if mydict is not None:
            for key in mydict:
                self.__setattr__(key, mydict[key])

    def __str__(self):
        return prettyJson(self)

class CityMeas(myBase):
    __tablename__ = 'cityMeas'

    id = Column(BigInteger, primary_key=True)
    location = Column(String(128))
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    uvi = Column(Float)
    wind_speed = Column(Float)
    wind_degree = Column(Integer)
    pop = Column(Float)
    measurementId = Column(BigInteger, ForeignKey('measurement.id'))
    measurement = relationship("Measurement", back_populates="cityMeas")

    def populate(self, arg):
        if type(arg) is dict:
            mydict = arg
        else:
            mydict = arg.__dict__

        if mydict is not None:
            for key in mydict:
                self.__setattr__(key, mydict[key])

    def __str__(self):
        return prettyJson(self)

class HomeMeas(myBase):
    __tablename__ = 'homeMeas'

    id = Column(BigInteger, primary_key=True)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    gas_resistance = Column(Float)
    eco2 = Column(Float)
    tvoc = Column(Float)
    measurementId = Column(BigInteger, ForeignKey('measurement.id'))
    measurement = relationship("Measurement", back_populates="homeMeas")

    def populate(self, arg):
        if type(arg) is dict:
            mydict = arg
        else:
            mydict = arg.__dict__

        if mydict is not None:
            for key in mydict:
                self.__setattr__(key, mydict[key])

    def __str__(self):
        return prettyJson(self)
