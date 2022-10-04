import numpy
from const import SPEED_OF_LIGHT as VC


# x1, y1 - observer position
# x2, y2, td2, v2, a2 - object position, time delta = current time - object observation time,
# velocity and velocity direction
#
# result light travel time and object position as it seen by observer
def calc_observed(x1, y1, observed_x2, observed_y2, td2, v2, a2):
    v2x = v2 * numpy.cos(a2)
    v2y = v2 * numpy.sin(a2)

    x2 = observed_x2 + v2x * td2
    y2 = observed_y2 + v2y * td2

    dx = x2-x1
    dy = y2-y1
    l2 = dx*dx + dy*dy

    A = v2*v2 - VC*VC
    B = 2*(dx*v2x + dy*v2y)
    C = l2

    solutions = numpy.roots([A, B, C])

    reals = list(filter(lambda x: not numpy.iscomplex(x) and x <= 0, solutions))

    if len(reals) > 0:
        time = min(reals)
        return [time, x2 + time * v2x, y2 + time * v2y]

    return []
