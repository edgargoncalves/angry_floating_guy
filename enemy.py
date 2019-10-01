"""asd"""

from random import choice, randrange
from drawable_item import DrawableItem


class Enemy(DrawableItem):
    """Enemy is something that moves..."""

    def __init__(self, hero, boundaries):
        self.hero = hero
        super(Enemy, self).__init__('batwing.png', boundaries)

    def move(self):
        signal = {'hori': choice((-1, 1)),
                  'vert': choice((-1, 1))}
        self.position['hori'] = self.hero.position['hori'] + \
            signal['hori']*50+signal['hori'] * randrange(0, 100)
        self.position['vert'] = self.hero.position['vert'] + \
            signal['vert']*50+signal['vert'] * randrange(0, 100)
