import arcade
from leg import Leg


class Ship:

    def __init__(self, initial_x, initial_y, current_time):
        self.center_x = initial_x
        self.center_y = initial_y
        self.radius = 10
        self.color = arcade.color.DARK_BROWN
        self.route = [Leg(initial_x, initial_y, initial_x, initial_y, current_time, 0)]
        self.outline = False

    def update(self, current_time):
        leg_index = self.find_current_leg_index(current_time)
        leg = self.route[leg_index]
        if leg.start_time <= current_time <= leg.stop_time and leg.stop_time - leg.start_time > 0:
            fraction = (current_time - leg.start_time) / (leg.stop_time - leg.start_time)
            self.center_x = leg.from_x + fraction * leg.dx
            self.center_y = leg.from_y + fraction * leg.dy
        else:
            self.center_x = self.route[leg_index].to_x
            self.center_y = self.route[leg_index].to_y

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, self.color)
        if self.outline:
            arcade.draw_circle_outline(self.center_x, self.center_y, self.radius + 2, self.color)

    def find_current_leg_index(self, current_time):
        l = len(self.route)
        index = l - 1
        while index > 0 and self.route[index].start_time >= current_time:
            index -= 1
        return index
