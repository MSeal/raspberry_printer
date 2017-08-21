class FakeI2C(object):
    def __init__(self, address, **kwargs):
        self.address = address
        self.clear_trackers()
        self.connect()

    def clear_trackers(self):
        self.registers = []
        self.values = []

    def disconnect(self):
        self.connected = False

    def connect(self):
        self.connected = True

    @staticmethod
    def get_i2c_device(address, **kwargs):
        return FakeI2C(address, **kwargs)

    def writeList(self, register, value):
        if not self.connected:
            raise IOError('Device is disconnected')
        self.registers.append(register)
        self.values.append(value)

    def write8(self, register, value):
        if not self.connected:
            raise IOError('Device is disconnected')
        self.registers.append(register)
        self.values.append(value)
