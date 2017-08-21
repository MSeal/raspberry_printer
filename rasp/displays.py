from Adafruit_LED_Backpack import AlphaNum4

class DisplayManager(object):
    def __init__(self, **displays):
        self.displays = {}
        for name, addr in displays.items():
            self.register_display(name, addr)

    def register_display(self, name, address=0x70, **kwargs):
        for check_name, check_disp in self.displays.items():
            if check_name == name:
                raise ValueError("Display name '{}' already taken".format(name))
            if check_disp._device.address == address:
                raise ValueError("Address ({}) already bound with '{}' display".format(address, check_name))
        disp = self.displays[name] = AlphaNum4.AlphaNum4(address=address, **kwargs)
        disp.started = False
        return disp

    def start_display(self, name):
        disp = self.displays[name]
        disp.begin()
        disp.clear()
        disp.started = True
        return disp

    def clear_all(self):
        for name, disp in self.displays.items():
            self.displays[name].clear()

    def write_all(self):
        for name, disp in self.displays.items():
            try:
                if not disp.started:
                    self.start_display(name)
                disp.write_display()
            except IOError:
                disp.started = False
