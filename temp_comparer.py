import RPi.GPIO as GPIO

class TempComparer:
    def __init__(self, hold_temp=75, temp_range=1):
        self.hold_temp = hold_temp
        self.temp_range = temp_range

    def compare_temps(self, current_temp, heater_pin):
        current_state = GPIO.input(heater_pin)
        print("Current State", current_state)
        print("Current Temp", current_temp)
        print("Hold Temp", self.hold_temp)
        if self.hold_temp >= current_temp + self.temp_range:
            return GPIO.HIGH
        elif self.hold_temp > current_temp and current_state == GPIO.HIGH:
            return GPIO.HIGH
        else:
            return GPIO.LOW

    def set_hold_temp(self, hold_temp):
        self.hold_temp = hold_temp

    def get_hold_temp(self):
        return self.hold_temp

    
        


