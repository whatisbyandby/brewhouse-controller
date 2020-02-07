import RPi.GPIO as GPIO

class PinController:
    def __init__(self):
        self.pump_one_pin = 8
        self.pump_two_pin = 12
        self.heater_pin = 10
        self.pump_one_state = GPIO.HIGH
        self.pump_two_state = GPIO.LOW
        self.heater_pin_state = GPIO.LOW
        self.pin_init()
        

    def cycle_pump_one(self, state):
        GPIO.output(self.pump_one_pin, state)

    def cycle_pump_two(self, state):
        GPIO.output(self.pump_two_pin, state)

    def cycle_heater(self, state):
        if state == GPIO.HIGH and self.pump_one_state == GPIO.HIGH:
            GPIO.output(self.heater_pin, GPIO.HIGH)
        elif state == GPIO.HIGH and self.pump_one_state == GPIO.LOW:
            raise Exception
        elif state == GPIO.LOW:
            GPIO.output(self.heater_pin, GPIO.LOW)

    def get_heater_pin(self):
        return self.heater_pin
        
    def pin_init(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup([self.pump_one_pin, self.pump_two_pin, self.heater_pin], GPIO.OUT, initial=GPIO.LOW)
