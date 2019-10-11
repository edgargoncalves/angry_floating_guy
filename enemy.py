"""asd"""

# from random import choice, randrange
from math import sin, cos
from drawable_item import DrawableItem
from random import randrange


class Enemy(DrawableItem):
    """Enemy is something that moves..."""

    def __init__(self, hero, background):
        self.hero = hero
        super(Enemy, self).__init__('batwing.png', background.boundaries)
        self.background = 0
        self.background = background

        self.angle = 0
        self.delay = 0
        self.position['vert'] = background.size['h']/2

    def move(self):

        self.angle = (self.angle + randrange(-1, 1)) % 360  # circle the hero

        if self.background.x > -self.size['w']:
            self.position['hori'] = self.background.x
        else:
            self.position['hori'] = self.background.x1

        self.position['hori'] += cos(self.angle)*50
        self.position['vert'] += sin(self.angle)*50

        self.delay = self.delay % 10
        vertical_displacement = randrange(-100, 100) if self.delay == 0 else 0

        bottom = self.background.size['h']-self.size['h']
        if not (0 <= self.position['vert']+vertical_displacement <= bottom):
            vertical_displacement *= -1

        self.position['vert'] += vertical_displacement

        self.position['vert'] = max(0, self.position['vert'])
        self.position['vert'] = min(bottom, self.position['vert'])
