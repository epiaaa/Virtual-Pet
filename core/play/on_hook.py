import time
import threading


class OnHook:
    def __init__(self):
        super().__init__()

    def hook_experience(self, start_time=0.0, end_time=10.0):
        hook_time = (end_time - start_time)/60
        experience = int(hook_time*1)
        self.gain_total_experience += experience
        self.experience += experience
        print('pet gain experience:', self.experience)

