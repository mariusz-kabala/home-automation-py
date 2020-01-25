from threading import Timer
from sensedashboard.sense import sense
from sensedashboard.helpers import set_interval
import time
from .face import show_smiley_face, show_frowning_face
from .clock import show_time


class Display:
    def __init__(self, mqtt):
        self.client = mqtt
        self.isOn = True
        self.extra_to_show = ""
        self.conditions = True
        self.on()

    def off(self):
        self.interval.cancel()
        sense.clear()

        self.isOn = False

    def on(self):
        if self.isOn:
            return

        self.isOn = True
        self.extra_to_show = ""
        self.conditions = True
        self.interval = set_interval(lambda: self.show(), 1)

    def show_msg(self, message: str, times: int = 3):
        self.interval.cancel()
        
        for x in range(times):
            sense.show_message(message)

        self.interval = set_interval(lambda: self.show(), 1)

    def set_conditions(self, value):
        self.conditions = value

    def clear_extra(self):
        self.extra_to_show = ""

    def show_alert(self):
        self.extra_to_show = "!"
        t = Timer(10.0, self.clear_extra)
        t.start()

    def show_conditions(self):
        if self.conditions:
            show_smiley_face(sense)
        else:
            show_frowning_face(sense)

    def show_time_and_conditions(self):
        sec = time.localtime().tm_sec
        if (sec % 5) == 0:
            self.show_conditions()
        else:
            show_time(sense)

    def show(self):
        if self.extra_to_show != "":
            sec = time.localtime().tm_sec
            if (sec % 2) == 0:
                sense.show_letter(self.extra_to_show, [255, 0, 0])
            else:
                show_time(sense)
        else:
            self.show_time_and_conditions()
