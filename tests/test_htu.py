# This import fixes sys.path issues
from . import parentpath

import unittest
import time
from mock import patch, MagicMock
from .fake_i2c import FakeI2C
from rasp.htu import (
    HTU21,
    HTU21DF_READTEMP,
    HTU21DF_READHUM,
    HTU21DF_WRITEREG,
    HTU21DF_READREG,
    HTU21DF_RESET
)

@patch('time.sleep', return_value=None)
class DisplayManagerTest(unittest.TestCase):
    def setUp(self):
        self.htu = HTU21(i2c=FakeI2C)
        self.i2c = self.htu._device

    def test_reset(self, patched_sleep):
        self.i2c.set_response(0x2)
        value = self.htu.reset()
        self.assertItemsEqual(self.i2c.values, [
            # Device startup
            HTU21DF_RESET,
            # Fetch status
            HTU21DF_READREG
        ])
        self.assertEqual(value, True)
        patched_sleep.assert_called_once_with(0.015)

    def test_start_sensor(self, patched_sleep):
        self.htu.reset = MagicMock()
        self.htu.start_sensor()
        self.htu.reset.assert_called_once()
        self.assertItemsEqual(self.i2c.values, [])

    def test_read_temperature(self, patched_sleep):
        self.i2c.set_response(int((25.12 + 46.85) * 65536 / 175.71))
        t = self.htu.read_temperature()
        self.assertAlmostEqual(t, 25.12, 2)
        patched_sleep.assert_called_once_with(0.05)

    def test_humidity(self, patched_sleep):
        self.i2c.set_response(int((50.00 + 6) * 65536 / 125))
        h = self.htu.read_humidity()
        self.assertAlmostEqual(h, 50.00, 2)
        patched_sleep.assert_called_once_with(0.05)
