from position import calc_observed
from const import SPEED_OF_LIGHT
import numpy
from ship import Ship
import arcade

observer = Ship(100, 400, 0)

boulder = Ship(500, 300, 0)
boulder.outline = True
boulder.add_leg(50, 400, 10, SPEED_OF_LIGHT * 0.9)
boulder.add_leg(50, 700, 40, SPEED_OF_LIGHT * 0.9)
# boulder.add_leg(600, 500, 60, SPEED_OF_LIGHT * 0.9)

arcade.open_window(800, 800)
arcade.set_background_color(arcade.color.WHITE)
arcade.start_render()
for x in boulder.route:
    arcade.draw_line(x.from_x, x.from_y, x.to_x, x.to_y, arcade.color.BLACK, 1)
arcade.draw_circle_filled(100, 400, 3, arcade.color.BLACK)

colors = [
    arcade.color.RED,
    arcade.color.YELLOW,
    arcade.color.GREEN,
    arcade.color.BLUE
]

for x in range(60):
    # print("")
    t = 2*x
    boulder.update(t)

    outline_leg_index = -1
    prev_solution = 'none'
    for index, leg in enumerate(boulder.route):
        td = t - leg.start_time
        if td >= 0 and leg.stop_time-leg.start_time > 0: # not in the future, moved
            a2 = numpy.arctan2(leg.dy, leg.dx)
            result = calc_observed(100, 400, leg.from_x, leg.from_y, td, leg.speed, a2)
            solution_time = t + result[0]
            if leg.stop_time >= solution_time >= leg.start_time:
                outline_leg_index = index
                boulder.outline_x = result[1]
                boulder.outline_y = result[2]
            elif leg.stop_time < solution_time:
                prev_solution = 'future'
            elif solution_time < leg.start_time:
                if prev_solution == 'future':
                    outline_leg_index = index
                    boulder.outline_x = leg.from_x
                    boulder.outline_y = leg.from_y
                prev_solution = 'past'

    if outline_leg_index == -1 and (prev_solution == 'none' or prev_solution == 'past'):
        outline_leg_index = 0
        boulder.outline_x = boulder.route[0].from_x
        boulder.outline_y = boulder.route[0].from_y

    if outline_leg_index == -1 and prev_solution == 'future':
        outline_leg_index = len(boulder.route)-1
        boulder.outline_x = boulder.route[-1].to_x
        boulder.outline_y = boulder.route[-1].to_y

    if outline_leg_index == -1:
        print("T=%7.2f %7.2f %7.2f S%d" % (t, boulder.center_x, boulder.center_y, outline_leg_index))
    else:
        print("T=%7.2f %7.2f %7.2f  M%d-> %7.2f - %7.2f" % (t, boulder.center_x, boulder.center_y, outline_leg_index, boulder.outline_x, boulder.outline_y))

    arcade.draw_circle_outline(boulder.outline_x, boulder.outline_y, 10, colors[outline_leg_index], 2)
    arcade.draw_text("{:.2f}".format(t), boulder.outline_x, boulder.outline_y, arcade.color.GRAY, 10)

arcade.finish_render()
arcade.run()
# result = calc_observed(5, 5, 10, 15, 3, 5, -numpy.pi/2)
#
# print('--------------------------------')
# print(result)
#
# print('X1', result[1], 'Y1', result[2])
# dist = numpy.sqrt( numpy.square(6-result[1]) + numpy.square(5-result[2]))
# print('Tl', dist)
# print('Tc', dist / SPEED_OF_LIGHT)