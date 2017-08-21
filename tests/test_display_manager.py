# This import fixes sys.path issues
from . import parentpath

import unittest
from .fake_i2c import FakeI2C
from rasp.displays import DisplayManager
from Adafruit_LED_Backpack import AlphaNum4, HT16K33
from Adafruit_LED_Backpack.HT16K33 import (
    HT16K33_SYSTEM_SETUP,
    HT16K33_OSCILLATOR,
    HT16K33_BLINK_CMD,
    HT16K33_BLINK_DISPLAYON,
    HT16K33_BLINK_OFF,
    HT16K33_CMD_BRIGHTNESS
)

class DisplayManagerTest(unittest.TestCase):
    def setUp(self):
        self.dm = DisplayManager()
        self.first = self.dm.register_display('first', 0x70, i2c=FakeI2C)
        self.second = self.dm.register_display('second', 0x71, i2c=FakeI2C)

    def test_register_same_addres(self):
        with self.assertRaises(ValueError):
            self.dm.register_display('fail', 0x70)

    def test_register_same_name(self):
        with self.assertRaises(ValueError):
            self.dm.register_display('first', 0x72)

    def test_start_display(self):
        self.dm.start_display('first')
        registers = self.first._device.registers
        self.assertItemsEqual(registers, [
            # Oscillator startup
            HT16K33_SYSTEM_SETUP | HT16K33_OSCILLATOR,
            # Blink off
            HT16K33_BLINK_CMD | HT16K33_BLINK_DISPLAYON | HT16K33_BLINK_OFF,
            # Max brightness
            HT16K33_CMD_BRIGHTNESS | 15
        ])

    def test_clear_all(self):
        for disp in self.dm.displays.values():
            disp.print_str('fill')
            self.assertNotEqual(bytearray([0]*16), disp.buffer)
        self.dm.clear_all()
        for disp in self.dm.displays.values():
            self.assertEqual(bytearray([0]*16), disp.buffer)

    def test_write_all_starts_displays(self):
        for disp in self.dm.displays.values():
            self.assertFalse(disp.started)
        self.dm.write_all()
        for disp in self.dm.displays.values():
            start_regs = disp._device.registers[:3]
            self.assertItemsEqual(start_regs, [
                # Oscillator startup
                HT16K33_SYSTEM_SETUP | HT16K33_OSCILLATOR,
                # Blink off
                HT16K33_BLINK_CMD | HT16K33_BLINK_DISPLAYON | HT16K33_BLINK_OFF,
                # Max brightness
                HT16K33_CMD_BRIGHTNESS | 15
            ])

    def test_write_all_pushes_buffers(self):
        self.dm.write_all() # trigger starts
        for index, disp in enumerate(self.dm.displays.values()):
            disp._device.clear_trackers() # remove startup noise
            self.assertEqual(bytearray([0]*16), disp.buffer)
            disp.print_float(index)
            self.assertNotEqual(bytearray([0]*16), disp.buffer)
            self.assertEqual([], disp._device.registers)
        self.dm.write_all()
        for disp in self.dm.displays.values():
            self.assertNotEqual([], disp._device.registers)

    def test_write_all_skips_discons(self):
        self.first._device.disconnect()
        self.second.print_str(' ON ')
        self.dm.write_all() # This should not crash despite IOErrors
        self.assertEqual([], self.first._device.registers)
        self.assertNotEqual([], self.second._device.registers)

    def test_write_all_sets_discon_off(self):
        self.dm.write_all()
        self.first._device.disconnect()
        self.dm.write_all() # This should not crash despite IOErrors
        self.assertFalse(self.first.started)
        self.assertTrue(self.second.started)
