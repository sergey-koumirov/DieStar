import arcade
import math
import numpy

from const import SPEED_OF_LIGHT


class Telemetry:

    ACTIVE = 1
    DONE = 2

    def __init__(self, from_x, from_y, to_x, to_y, start_time):
        self.center_x = 0
        self.center_y = 0
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.speed = SPEED_OF_LIGHT
        self.dx = to_x - from_x
        self.dy = to_y - from_y
        self.direction = numpy.arctan2(self.dy, self.dx)
        self.start_time = start_time
        self.stop_time = start_time + math.sqrt(self.dx*self.dx + self.dy*self.dy) / SPEED_OF_LIGHT
        self.state = self.ACTIVE

    def update(self, current_time):
        if self.state == self.DONE:
            return
        elif current_time > self.stop_time:
            self.state = self.DONE
            self.center_x = self.from_x
            self.center_y = self.from_y
        else:
            fraction = (current_time - self.start_time) / (self.stop_time - self.start_time)
            self.center_x = self.from_x + fraction * self.dx
            self.center_y = self.from_y + fraction * self.dy

    def draw(self):
        if self.state == self.DONE:
            arcade.draw_line(self.from_x, self.from_y, self.to_x, self.to_y, arcade.color.GRAY)
        else:
            arcade.draw_line(self.from_x, self.from_y, self.to_x, self.to_y, arcade.color.GOLDENROD)
            arcade.draw_circle_outline(self.center_x, self.center_y, 3, arcade.color.GOLD)

