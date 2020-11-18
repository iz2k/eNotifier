import json
import os
from urllib import request
from PIL import Image,ImageDraw,ImageFont

from eNotifierBackend.epd75bv2.epdCtl import epdCtl
from eNotifierBackend.tools.imgTools import reseizeImage
from eNotifierBackend.tools.jsonTools import writeJsonFile, readJsonFile, prettyJson


class WeatherStation:

    config = {}
    report = {}

    epd = epdCtl()

    def __init__(self):
        self.loadConfig()
        self.printConfig()
        self.updateWeatherReport()
        self.updateEpd()

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
            self.report = json.loads(con.read().decode())
        print('Weather Station Report Update:')
        print(prettyJson(
            {
                'location' : self.config['location'],
                'temperature' : str(self.report['current']['temp']) + 'C',
                'pressure' : str(self.report['current']['pressure']) + 'mbar',
                'humidity' : str(self.report['current']['humidity']) + '%',
                'weather' : self.report['current']['weather'][0]['description']
            }
        ))
        print(prettyJson(self.report))
        return self.report

    def updateEpd(self):
        picdir = 'pic'
        font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

        imageBlack = Image.new('1', (self.epd.SCREEN_WIDTH, self.epd.SCREEN_HEIGHT), 255)  # 255: clear the frame
        imageRed = Image.new('1', (self.epd.SCREEN_WIDTH, self.epd.SCREEN_HEIGHT), 255)  # 255: clear the frame
        drawBlack = ImageDraw.Draw(imageBlack)
        drawRed = ImageDraw.Draw(imageRed)

        imageRed.paste(Image.open(os.path.join(picdir, 'home.png'))
                       , (30, 30))
        drawBlack.text((110, 38), 'Etxean', font=font48, fill=0)

        imageBlack.paste(Image.open(os.path.join(picdir, 'thermo.png'))
                         , (50, 130))
        drawRed.text((130, 138), '25.6ºC', font=font48, fill=0)

        imageBlack.paste(Image.open(os.path.join(picdir, 'hygro.png'))
                         , (50, 210))
        drawRed.text((130, 218), '58%', font=font48, fill=0)

        imageBlack.paste(Image.open(os.path.join(picdir, 'pressure.png'))
                         , (50, 290))
        drawRed.text((130, 298), '1002mb', font=font48, fill=0)

        imageBlack.paste(Image.open(os.path.join(picdir, 'air.png'))
                         , (50, 370))
        drawRed.text((130, 378), '32', font=font48, fill=0)

        imageBlack.paste(Image.open(os.path.join(picdir, 'city.png'))
                         , (700, 30))
        drawRed.text((460, 38), 'Donostian', font=font48, fill=0)

        imageBlack.paste(Image.open(os.path.join(picdir, 'weather/03-partly-cloudy-day.png'))
                         , (520, 120))

        imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'thermo.png')), (32, 32))
                       , (450, 270))
        drawBlack.text((490, 274), str(self.report['current']['temp']) + 'ºC', font=font24, fill=0)

        imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'pressure.png')), (32, 32))
                       , (600, 270))
        drawBlack.text((640, 274), str(self.report['current']['pressure']) + 'mb', font=font24, fill=0)

        imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'hygro.png')), (32, 32))
                       , (450, 320))
        drawBlack.text((490, 324), str(self.report['current']['humidity']) + '%', font=font24, fill=0)

        imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'air.png')), (32, 32))
                       , (600, 320))
        drawBlack.text((640, 324), '39', font=font24, fill=0)

        imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'wind.png')), (32, 32))
                       , (450, 370))
        try:
            wind = self.report['current']['wind_gust']
        except:
            wind = self.report['current']['wind_speed']
        drawBlack.text((490, 374), str(int(round(wind*3.6))) + 'km/h', font=font24, fill=0)

        imageRed.paste(reseizeImage(Image.open(os.path.join(picdir, 'rain.png')), (32, 32))
                       , (600, 370))
        drawBlack.text((640, 374), str(self.report['hourly'][0]['pop']) + '%', font=font24, fill=0)

        drawBlack.rectangle((490, 440, 800, 480), fill=0)
        drawBlack.polygon([(490, 440), (490, 480), (460, 480)], fill=0)
        drawBlack.text((500, 445), 'Azken neurketa:', font=font24, fill=1)
        drawRed.text((700, 445), '16:15', font=font24, fill=0)

        self.epd.display(imageBlack, imageRed)
