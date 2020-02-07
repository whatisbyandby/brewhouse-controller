from w1thermsensor import W1ThermSensor

class TempReader:
    def __init__(self, units=W1ThermSensor.DEGREES_F):
        self.units = units
        self.sensor = W1ThermSensor()

    def get_current_temp(self):
        current_temp = round(self.sensor.get_temperature(self.units), 2)
        return current_temp