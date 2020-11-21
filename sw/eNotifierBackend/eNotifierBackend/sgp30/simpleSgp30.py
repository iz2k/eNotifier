import time
import busio
import board
import adafruit_sgp30
from adafruit_bus_device.i2c_device import I2CDevice


class SimpleSGP30():

    def __init__(self, baseline):
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(busio.I2C(board.SCL, board.SDA, frequency=100000))
        self.initConfig(baseline)

    def initConfig(self, baseline):
        self.sgp30.iaq_init()
        self.sgp30.set_iaq_baseline(baseline[0], baseline[1])

    def getSensorData(self):
        return {
            'eCO2' : self.sgp30.eCO2,
            'TVOC' : self.sgp30.TVOC,
            'baseline': self.sgp30.get_iaq_baseline()
        }

    def getBaseline(self):
        return {
            'baseline' : self.sgp30.get_iaq_baseline()
        }

    def resetBaseline(self):
        self.resetDevice()
        self.sgp30.iaq_init()
        return {
            'baseline' : self.sgp30.get_iaq_baseline()
        }


    def resetDevice(self):
        dev = I2CDevice(busio.I2C(board.SCL, board.SDA, frequency=100000), 0x00)
        dev.write(bytes(0x00))
        time.sleep(1)

    def adjustRH(self, RH):
        H = self.fakeRH2H(RH)
        print('Adjusting IAQ with H: ' + str(H) + 'g/m3')
        self.sgp30.set_iaq_humidity(H)

    def fakeRH2H(self, RH):
        # Assuming ~20ºC and 1000mbar
        H = 17*RH/100 #g/m3
        return H