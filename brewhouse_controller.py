import time
import datetime
from threading import Thread

class BrewhouseController:
    def __init__(self):
        self.steps = []
        self.current_step = 0
        self.current_start_time = None
        self.current_step_length = None
        self.tick_interval = 1
        self.running = False
        self.loop_thread = Thread(target=self.main_loop)
        
    def set_steps(self, steps):
        self.steps = steps
        return self.steps

    def get_steps(self):
        return self.steps

    def get_current_step(self):
        return self.current_step

    def get_step_by_index(self, index):
        try:
            step = self.steps[index]
            return step
        except IndexError:
            return None
        
    def update_step(self, index, step):
        try:
            self.steps[index] = step
        except IndexError:
            return None

    def delete_step(self, index):
        try:
            del self.steps[index]
            return True
        except IndexError:
            return False

    def run(self):
        if not self.running:
            self.next_step()
            self.running = True
            self.loop_thread.start()
            return True
        else: 
            return False
    
    def stop(self):
        if self.running:
            self.running = False
            self.loop_thread.join()
            self.loop_thread = Thread(target=self.main_loop)
            return True
        else:
            return False

    def next_step(self):
        self.current_start_time = datetime.datetime.now()
        self.current_step_length = datetime.timedelta(seconds=self.steps[self.current_step]["hold_time"])

    def main_loop(self):
        while self.running:
            time.sleep(1)
            time_passed = datetime.datetime.now() - self.current_start_time
            if time_passed > self.current_step_length:
                self.current_step = self.current_step + 1
                if len(self.steps) > self.current_step:
                    self.next_step()
                else:
                    self.running = False
                    self.current_step = 0
            print(time_passed)




    

    
        