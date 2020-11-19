import time
import busio
import board
import adafruit_sgp30

class SimpleSGP30():

    def __init__(self):
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(busio.I2C(board.SCL, board.SDA, frequency=100000))
        self.initConfig()

    def initConfig(self):
        self.sgp30.iaq_init()
        #self.sgp30.set_iaq_baseline(40000, 35502)

    def getSensorData(self):
        return {
            'eCO2' : self.sgp30.eCO2,
            'TVOC' : self.sgp30.TVOC,
        }

    def getBaseline(self):
        return {
            'baseline' : self.sgp30.get_iaq_baseline()
        }
