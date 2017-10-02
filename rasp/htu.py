import time

HTU21DF_I2CADDR = 0x40
HTU21DF_READTEMP = 0xE3
HTU21DF_READHUM = 0xE5
HTU21DF_WRITEREG = 0xE6
HTU21DF_READREG = 0xE7
HTU21DF_RESET = 0xFE

class HTU21(object):
    def __init__(self, i2c=None, **kwargs):
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(HTU21DF_I2CADDR, **kwargs)

    def start_sensor(self):
        return self.reset()

    def reset(self):
        self._device.writeRaw8(HTU21DF_RESET)
        time.sleep(0.015)
        self._device.writeRaw8(HTU21DF_READREG)
        return self._device.readRaw8() == 0x2

    def read_temperature(self):
        self._device.writeRaw8(HTU21DF_READTEMP)
        time.sleep(0.05)
        t = float(self._device.readU16())
        return (t * 175.72 / 65536) - 46.85

    def read_humidity(self):
        self._device.writeRaw8(HTU21DF_READHUM)
        time.sleep(0.05)
        h = float(self._device.readU16())
        return (h * 125 / 65536) - 6
