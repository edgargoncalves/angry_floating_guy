"""asd"""

# from random import choice, randrange
from math import sin, cos
from drawable_item import DrawableItem


class Enemy(DrawableItem):
    """Enemy is something that moves..."""

    def __init__(self, hero, boundaries):
        self.hero = hero
        super(Enemy, self).__init__('batwing.png', boundaries)
        self.angle = 0

    def move(self):

        self.angle = (self.angle+.1) % 360  # circle the hero

        self.position['hori'] = self.hero.position['hori'] + \
            cos(self.angle)*100
        self.position['vert'] = self.hero.position['vert'] + \
            sin(self.angle)*100
