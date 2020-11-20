import json
from datetime import datetime
from urllib import request

from eNotifierBackend.bme680.simpleBme680 import SimpleBME680
from eNotifierBackend.dbManager import Measurement, CityMeas, HomeMeas
from eNotifierBackend.dbManager.dbController import dbController
from eNotifierBackend.epd75bv2.epdCtl import epdCtl
from eNotifierBackend.sgp30.simpleSgp30 import SimpleSGP30
from eNotifierBackend.tools.jsonTools import writeJsonFile, readJsonFile, prettyJson
from eNotifierBackend.weatherStation.weatherHomeScreen import weatherHomeScreen


class WeatherStation:

    config = {}
    weatherReport = {}
    sensorReport = {}

    bme = None
    sgp = None
    epd = None

    def __init__(self, dbctl : dbController):
        self.loadConfig()
        self.printConfig()
        self.epd = epdCtl()
        self.bme = SimpleBME680()
        self.sgp = SimpleSGP30([int(self.config['baselineEco2']), int(self.config['baselineTvoc'])])
        self.dbctl = dbctl

    def saveConfig(self):
        writeJsonFile('cfgWeatherStation.json', self.config)

    def loadConfig(self):
        self.config = readJsonFile('cfgWeatherStation.json')
        if self.config == {}:
            self.createDefaultConfig()

    def reloadConfig(self):
        self.loadConfig()
        self.printConfig()
        self.sgp.resetDevice()
        self.sgp.initConfig([int(self.config['baselineEco2']), int(self.config['baselineTvoc'])])


    def printConfig(self):
        print('Weather Station Config:')
        print(prettyJson(self.config))

    def createDefaultConfig(self):
        self.config = {
            'openWeatherApi': '***REMOVED***',
            'geocodeApi': '',
            'location': '',
            'cityAlias': '',
            'longitude': 0,
            'latitude': 0,
            'baselineEco2': 34274,
            'baselineTvoc': 34723
                       }
        self.saveConfig()

    def updateParam(self, param, value):
        self.config[param]=value
        self.saveConfig()

    def updateWeatherReport(self):
        url = 'https://api.openweathermap.org/data/2.5/onecall?'
        url = url + 'lat=' + str(self.config['latitude']) + '&'
        url = url + 'lon=' + str(self.config['longitude']) + '&'
        url = url + 'exclude=minutely&'
        url = url + 'units=metric&'
        url = url + 'lang=es&'
        url = url + 'appid=' + self.config['openWeatherApi']

        with request.urlopen(url) as con:
            self.weatherReport = json.loads(con.read().decode())
        print('Weather Station Report Update:')
        print(prettyJson(
            {
                'location' : self.config['location'],
                'temperature' : str(self.weatherReport['current']['temp']) + 'C',
                'pressure' : str(self.weatherReport['current']['pressure']) + 'mbar',
                'humidity' : str(self.weatherReport['current']['humidity']) + '%',
                'weather' : self.weatherReport['current']['weather'][0]['description']
            }
        ))
        print(self.weatherReport)

    def updateEpd(self):
        weatherHomeScreen(self.epd, self.weatherReport, self.sensorReport, self.config)

    def updateSensorReport(self):
        self.sensorReport = {}
        bmedata = {}
        while bmedata == {}:
            bmedata = self.bme.getSensorData()

        for parameter in bmedata:
            self.sensorReport[parameter] = bmedata[parameter]
        sgpdata = self.sgp.getSensorData()
        for parameter in sgpdata:
            self.sensorReport[parameter] = sgpdata[parameter]
        print(self.sensorReport)

    def insertToDb(self):
        myMeas = Measurement(
            datetime=datetime.now(),
            cityMeas=CityMeas(
                location=self.config['location'],
                temperature=self.weatherReport['current']['temp'],
                pressure=self.weatherReport['current']['pressure'],
                humidity=self.weatherReport['current']['humidity'],
                uvi=self.weatherReport['current']['uvi'],
                wind_speed=self.weatherReport['current']['wind_speed'],
                wind_degree=self.weatherReport['current']['wind_deg'],
                pop=self.weatherReport['hourly'][0]['pop']
            ),
            homeMeas=HomeMeas(
                temperature=self.sensorReport['temperature'],
                pressure=self.sensorReport['pressure'],
                humidity=self.sensorReport['humidity'],
                gas_resistance=self.sensorReport['gas_resistance'],
                eco2=self.sensorReport['eCO2'],
                tvoc=self.sensorReport['TVOC']
            )
        )

        self.dbctl.insert(myMeas)
