import json
from urllib import request

from eNotifierBackend.bme680.simpleBme680 import SimpleBME680
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

    def __init__(self):
        self.loadConfig()
        self.printConfig()
        self.epd = epdCtl()
        self.bme = SimpleBME680()
        self.sgp = SimpleSGP30()

    def saveConfig(self):
        writeJsonFile('cfgWeather.json', self.config)

    def loadConfig(self):
        self.config = readJsonFile('cfgWeather.json')
        if self.config == {}:
            self.createDefaultConfig()

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
            'latitude': 0
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
        weatherHomeScreen(self.epd, self.weatherReport, self.sensorReport)

    def updateSensorReport(self):
        self.sensorReport = {}
        bmedata = {}
        while bmedata == {}:
            print('getting bme data')
            bmedata = self.bme.getSensorData()

        for parameter in bmedata:
            self.sensorReport[parameter] = bmedata[parameter]
        sgpdata = self.sgp.getSensorData()
        for parameter in sgpdata:
            self.sensorReport[parameter] = sgpdata[parameter]
        print(self.sensorReport)
