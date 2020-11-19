from eNotifierBackend import bme680

class SimpleBME680:

    sensor = None

    def __init__(self):
        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except IOError:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

        self.initConfig()

    def printCalibrationData(self):
        for name in dir(self.sensor.calibration_data):

            if not name.startswith('_'):
                value = getattr(self.sensor.calibration_data, name)

                if isinstance(value, int):
                    print('{}: {}'.format(name, value))

    def initConfig(self):
        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)

    def getSensorData(self):
        data={}
        if self.sensor.get_sensor_data():
            data['temperature'] = self.sensor.data.temperature
            data['pressure'] = self.sensor.data.pressure
            data['humidity'] = self.sensor.data.humidity

            if self.sensor.data.heat_stable:
                data['gas_resistance'] = self.sensor.data.gas_resistance
            else:
                data['gas_resistance'] = 0

        return data
