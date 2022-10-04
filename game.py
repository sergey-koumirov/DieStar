import arcade
from leg import Leg
from ship import Ship
from telemetry import Telemetry
from const import SPEED_OF_LIGHT


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.time = 0
        self.last_emission_at = -1

        self.observer = Ship(100, 400, 0)
        self.observer.color = arcade.color.BLACK

        self.boulders = [Ship(500, 300, 0), Ship(500, 400, 0), Ship(100, 600, 0)]

        self.boulders[0].add_leg(0, 400, 0, SPEED_OF_LIGHT * 0.9)
        self.boulders[0].add_leg(600, 500, 29, SPEED_OF_LIGHT * 0.9)
        self.boulders[0].color = arcade.color.ANTIQUE_RUBY
        self.boulders[0].outline = True

        self.boulders[1].color = arcade.color.ANTIQUE_RUBY
        self.boulders[1].outline = True

        self.boulders[2].add_leg(600, 600, 0, SPEED_OF_LIGHT * 0.5)
        self.boulders[2].color = arcade.color.ANTIQUE_RUBY
        self.boulders[2].outline = True

        self.telemetry = []

        self.background_color = arcade.color.DIM_GRAY

    def time_to_shine(self):
        return self.time - self.last_emission_at > 2

    def on_update(self, delta_time):
        self.time += delta_time

        self.observer.update(delta_time, None)

        if self.time_to_shine():
            self.last_emission_at = self.time
            for x in self.boulders:
                temp = Telemetry(x.center_x, x.center_y, self.observer.center_x, self.observer.center_y, self.time)
                self.telemetry.append(temp)

        for x in self.boulders:
            x.update(self.time, self.observer)

        for x in self.telemetry:
            x.update(self.time)

        self.telemetry = list(filter(lambda t: t.state == Telemetry.ACTIVE or self.time - t.stop_time < 10, self.telemetry))

    def on_draw(self):
        self.clear()
        self.observer.draw()
        for x in self.boulders:
            x.draw()
        for x in self.telemetry:
            x.draw()
        arcade.draw_text( "{:.2f}".format(self.time), 50, 750, arcade.color.BLACK, 12)
