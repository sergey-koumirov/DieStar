import arcade
from leg import Leg
import numpy
from position import calc_observed

class Ship:

    SL_NONE = 0
    SL_FUTURE = 1
    SL_PAST = 2

    def __init__(self, initial_x, initial_y, current_time):
        self.center_x = initial_x
        self.center_y = initial_y
        self.outline_x = initial_x
        self.outline_y = initial_y
        self.radius = 10
        self.color = arcade.color.DARK_BROWN
        self.route = [Leg(initial_x, initial_y, initial_x, initial_y, current_time, 0)]
        self.outline = False

    def update(self, current_time, observer):
        leg_index = self.find_current_leg_index(current_time)
        leg = self.route[leg_index]
        if leg.start_time <= current_time <= leg.stop_time and leg.stop_time - leg.start_time > 0:
            fraction = (current_time - leg.start_time) / (leg.stop_time - leg.start_time)
            self.center_x = leg.from_x + fraction * leg.dx
            self.center_y = leg.from_y + fraction * leg.dy
        else:
            self.center_x = self.route[leg_index].to_x
            self.center_y = self.route[leg_index].to_y

        if self.outline:
            outline_position = self.get_outline_position(current_time, observer)
            self.outline_x = outline_position[0]
            self.outline_y = outline_position[1]

    def draw(self):
        arcade.draw_circle_outline(self.center_x, self.center_y, self.radius + 2, self.color, num_segments=8)
        if self.outline:
            arcade.draw_circle_filled(self.outline_x, self.outline_y, self.radius, self.color)

    def find_current_leg_index(self, current_time):
        l = len(self.route)
        index = l - 1
        while index > 0 and self.route[index].start_time >= current_time:
            index -= 1
        return index

    def add_leg(self, to_x, to_y, time, speed):
        if len(self.route) == 0:
            self.route.append(Leg(to_x, to_y, to_x, to_y, time, speed))
        else:
            last = self.route[-1]
            self.route.append(Leg(last.to_x, last.to_y, to_x, to_y, time, speed))

    def get_outline_position(self, current_time, observer):
        outline_leg_index = -1
        prev_solution = self.SL_NONE
        solution = [self.center_x, self.center_y]

        for index, leg in enumerate(self.route):
            td = current_time - leg.start_time
            if td >= 0 and leg.stop_time - leg.start_time > 0:  # not in the future, moved
                a2 = numpy.arctan2(leg.dy, leg.dx)
                result = calc_observed(observer.center_x, observer.center_y, leg.from_x, leg.from_y, td, leg.speed, a2)
                solution_time = current_time + result[0]
                if leg.stop_time >= solution_time >= leg.start_time:
                    outline_leg_index = index
                    solution[0] = result[1]
                    solution[1] = result[2]
                elif leg.stop_time < solution_time:
                    prev_solution = self.SL_FUTURE
                elif solution_time < leg.start_time:
                    if prev_solution == self.SL_FUTURE:
                        outline_leg_index = index
                        solution[0] = leg.from_x
                        solution[1] = leg.from_y
                    prev_solution = self.SL_PAST

        if outline_leg_index == -1 and (prev_solution == self.SL_NONE or prev_solution == self.SL_PAST):
            outline_leg_index = 0
            solution[0] = self.route[outline_leg_index].from_x
            solution[1] = self.route[outline_leg_index].from_y

        if outline_leg_index == -1 and prev_solution == self.SL_FUTURE:
            outline_leg_index = len(self.route) - 1
            solution[0] = self.route[outline_leg_index].to_x
            solution[1] = self.route[outline_leg_index].to_y

        return solution
