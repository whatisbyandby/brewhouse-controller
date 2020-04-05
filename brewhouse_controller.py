import time
from datetime import datetime, timedelta
from collections import namedtuple
from threading import Thread
from pin_controller import PinController
from temp_reader import TempReader
from temp_comparer import TempComparer

class BrewhouseController:
    def __init__(self):
        #self.steps = []
        self.current_temp = 0
        self.current_step = None
        #self.current_step_count = 0
        self.current_start_time = None
        self.current_step_length = None
        self.step_end_time = None
        self.temp_reader = TempReader()
        self.pin_controller = PinController()
        self.temp_comparer = TempComparer()
        self.tick_interval = 1
        self.running = False
        self.loop_thread = Thread(target=self.main_loop)
        self.loop_thread.start()

    def broadcast_data(self):
        if self.running and self.current_step is not None:
            time_remaining = self.step_end_time - datetime.now()
            minutes = str((time_remaining.seconds//60)%60).zfill(2)
            seconds = str(time_remaining.seconds % 60).zfill(2)
            return {
                "currentTemp": self.current_temp, 
                "running": self.running,
                "currentStep": self.current_step,
                "timeRemaining": "{}:{}".format(minutes, seconds)
                }
        else:
            return {
                "currentTemp": self.current_temp,
                "running": self.running,
                "currentStep": self.current_step,
                "timeRemaining": None
            }
        
        
    # def set_steps(self, steps):
    #     self.steps = steps
    #     return self.steps

    def set_step(self, step):
        self.current_step = step
        return self.current_step

    # def get_steps(self):
    #     return self.steps

    def get_current_step(self):
        return self.current_step

    # def get_step_by_index(self, index):
    #     try:
    #         step = self.steps[index]
    #         return step
    #     except IndexError:
    #         return None
        
    # def update_step(self, index, step):
    #     try:
    #         self.steps[index] = step
    #     except IndexError:
    #         return None

    def delete_step(self, index):
        try:
            del self.steps[index]
            return True
        except IndexError:
            return False

    def start(self):
        if not self.running and self.current_step is not None:
            self.step_end_time = datetime.now() + timedelta(minutes=self.current_step["holdTime"]) 
            print(self.step_end_time)
            self.running = True
            return True
        else: 
            return False
    
    def stop(self):
        if self.running:
            self.current_step = None
            self.running = False
            self.loop_thread = Thread(target=self.main_loop)
            return True
        else:
            return False

    def pause(self):
        pass

    def get_pump_state(self, id):
        pump_state = self.pin_controller.get_pump_state(id)
        return pump_state

    def cycle_pump_state(self, id):
        return self.pin_controller.cycle_pump_state(id)

    # def next_step(self):
    #     self.current_step = self.steps[self.current_step_count]
    #     self.current_start_time = datetime.datetime.now()
    #     self.current_step_length = datetime.timedelta(minutes=self.steps[self.current_step_count]["hold_time"])
    #     self.current_end_time = self.current_start_time + self.current_step_length
    #     self.temp_comparer.set_hold_temp(self.steps[self.current_step_count]["start_temp"])

    def main_loop(self):
        try:
            while True:
                self.current_temp = self.temp_reader.get_current_temp()
                if self.running:
                    new_state = self.temp_comparer.compare_temps(self.current_temp, self.pin_controller.get_heater_pin())
                    self.pin_controller.cycle_heater(new_state)
                    if datetime.now() > self.step_end_time:
                        self.current_step = None
                        self.running = False
                time.sleep(1)
        except Exception as e:
            print(e)
        finally:
            PinController.cleanup()
            




    

    
        