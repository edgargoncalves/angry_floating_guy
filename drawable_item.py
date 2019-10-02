"""asdad"""

import pygame
from pygame.locals import *


class DrawableItem():
    """A thing you  can draw on the screen."""

    def __init__(self, filename, boundaries, width=50, height=50):
        self.position = {'hori': 0, 'vert': 0}
        self.velocity = {'hori': 0, 'vert': 0}
        self.bodymass = 1
        self.image = None
        self.filename = filename
        self.size = {'h': width, 'w': height}
        self.moving = {pygame.K_DOWN: False,
                       pygame.K_UP: False,
                       pygame.K_LEFT: False,
                       pygame.K_RIGHT: False}
        self.boundaries = boundaries
        self.screen = None

    def scale(self, factor_h, factor_w):
        self.size['h'] *= factor_h
        self.size['w'] *= factor_w
        self.image = pygame.transform.scale(
            self.image, self.size['w'], self.size['h'])

    def load_from_file(self):
        self.image = pygame.transform.scale(
            pygame.image.load("images/"+self.filename),
            (self.size['w'], self.size['h'])).convert_alpha()

    def blit(self):
        self.screen.blit(
            self.image, (self.position['hori'],
                         self.position['vert']))

    def move(self):
        pass
