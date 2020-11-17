import time
import spidev
import RPi.GPIO

class epdCtl:

    PIN_RST = 17
    PIN_DC = 25
    PIN_CS = 8
    PIN_BUSY = 24
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 480

    def __init__(self):
        self.GPIO = RPi.GPIO
        self.SPI = spidev.SpiDev(0, 0)

        print('Initializing EPD')
        self._module_init()
        self._hw_reset()

        self._send_command(0x01)  # POWER SETTING
        self._send_data(0x07)
        self._send_data(0x07)  # VGH=20V,VGL=-20V
        self._send_data(0x3f)  # VDH=15V
        self._send_data(0x3f)  # VDL=-15V

        self._send_command(0x04)  # POWER ON
        self.delay_ms(100)
        self._wait_busy()

        self._send_command(0X00)  # PANNEL SETTING
        self._send_data(0x0F)  # KW-3f   KWR-2F	BWROTP 0f	BWOTP 1f

        self._send_command(0x61)  # tres
        self._send_data(0x03)  # source 800
        self._send_data(0x20)
        self._send_data(0x01)  # gate 480
        self._send_data(0xE0)

        self._send_command(0X15)
        self._send_data(0x00)

        self._send_command(0X50) # VCOM AND DATA INTERVAL SETTING
        self._send_data(0x11)
        self._send_data(0x07)

        self._send_command(0X60)  # TCON SETTING
        self._send_data(0x22)

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def _module_init(self):
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(self.PIN_RST, self.GPIO.OUT)
        self.GPIO.setup(self.PIN_DC, self.GPIO.OUT)
        self.GPIO.setup(self.PIN_CS, self.GPIO.OUT)
        self.GPIO.setup(self.PIN_BUSY, self.GPIO.IN)
        self.SPI.max_speed_hz = 4000000
        self.SPI.mode = 0b00

    def _module_exit(self):
        print("Module enters 0 power consumption ...")
        self.SPI.close()
        self.GPIO.output(self.PIN_RST, 0)
        self.GPIO.output(self.PIN_DC, 0)
        self.GPIO.cleanup()

    def _hw_reset(self):
        self.GPIO.output(self.PIN_RST, 1)
        self.delay_ms(200)
        self.GPIO.output(self.PIN_RST, 0)
        self.delay_ms(4)
        self.GPIO.output(self.PIN_RST, 1)
        self.delay_ms(200)

    def _send_command(self, command):
        self.GPIO.output(self.PIN_DC, 0)
        self.GPIO.output(self.PIN_CS, 0)
        self.SPI.writebytes([command])
        self.GPIO.output(self.PIN_CS, 1)

    def _send_data(self, data):
        self.GPIO.output(self.PIN_DC, 1)
        self.GPIO.output(self.PIN_CS, 0)
        self.SPI.writebytes([data])
        self.GPIO.output(self.PIN_CS, 1)

    def _wait_busy(self):
        self._send_command(0x71)
        busy = self.GPIO.input(self.PIN_BUSY)
        print('Waiting EPD to perform operation...', end='')
        while (busy == 0):
            self._send_command(0x71)
            busy = self.GPIO.input(self.PIN_BUSY)
        print(' Done!',)
        self.delay_ms(200)

    def _image_to_buffer(self, image):
        buf = [0xFF] * (int(self.SCREEN_WIDTH / 8) * self.SCREEN_HEIGHT)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        if (imwidth == self.SCREEN_WIDTH and imheight == self.SCREEN_HEIGHT):
            print("Creating Horizontal Image Buffer")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.SCREEN_WIDTH) / 8)] &= ~(0x80 >> (x % 8))
        elif (imwidth == self.SCREEN_HEIGHT and imheight == self.SCREEN_WIDTH):
            print("Creating Vertical Image Buffer")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.SCREEN_HEIGHT - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy * self.SCREEN_WIDTH) / 8)] &= ~(0x80 >> (y % 8))
        return buf

    def display(self, imageBlack, imageColor):
        bufferBlack = self._image_to_buffer(imageBlack)
        bufferColor = self._image_to_buffer(imageColor)
        self._send_command(0x10)
        for i in range(0, int(self.SCREEN_WIDTH * self.SCREEN_HEIGHT / 8)):
            self._send_data(bufferBlack[i]);

        self._send_command(0x13)
        for i in range(0, int(self.SCREEN_WIDTH * self.SCREEN_HEIGHT / 8)):
            self._send_data(~bufferColor[i]);

        self._send_command(0x12)
        self.delay_ms(100)
        self._wait_busy()

    def clear(self):
        self._send_command(0x10)
        for i in range(0, int(self.SCREEN_WIDTH * self.SCREEN_HEIGHT / 8)):
            self._send_data(0xff)

        self._send_command(0x13)
        for i in range(0, int(self.SCREEN_WIDTH * self.SCREEN_HEIGHT / 8)):
            self._send_data(0x00)

        self._send_command(0x12)
        self.delay_ms(100)
        self._wait_busy()

    def sleep(self):
        self._send_command(0x02)  # POWER_OFF
        self._wait_busy()

        self._send_command(0x07)  # DEEP_SLEEP
        self._send_data(0XA5)

        self._module_exit()

