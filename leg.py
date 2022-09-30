import math


class Leg:

    def __init__(self, from_x, from_y, to_x, to_y, start_time, speed):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.start_time = start_time
        self.speed = speed
        self.dx = to_x - from_x
        self.dy = to_y - from_y
        if speed == 0:
            self.stop_time = self.start_time
        else:
            self.stop_time = start_time + math.sqrt(self.dx * self.dx + self.dy * self.dy) / speed
