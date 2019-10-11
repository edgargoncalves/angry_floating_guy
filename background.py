"""A Background drawable class"""

import pygame
from pygame.locals import *
from drawable_item import DrawableItem


class Background(DrawableItem):
    """Documentation for Background."""

    def __init__(self, width, height):
        super(Background, self).__init__('background.png',
                                         boundaries={'hori': [0, width],
                                                     'vert': [0, height]},
                                         width=width,
                                         height=height)
        self.rect = None
        self.screen: None
        self.size = {'w': width, 'h': height}
        self.w = 0
        self.h = 0
        self.x = 0
        self.y = 0
        self.x1 = 0
        self.y1 = 0
        self.x_offset = 0
        self.fullscreen = False
        self.fps = 25

    def toggle_fullscreen(self):
        fullscreen_flag = pygame.FULLSCREEN if self.fullscreen else 0
        self.fullscreen = not self.fullscreen
        self.fps = 30 if self.fullscreen else 20

        self.screen = pygame.display.set_mode(
            (self.size['w'], self.size['h']),
            pygame.HWSURFACE  # | pygame.DOUBLEBUF
            | fullscreen_flag)
        self.screen.set_alpha(None)

    def load_from_file(self):
        self.image = pygame.transform.scale(
            pygame.image.load("images/"+self.filename),
            (self.size['w'], self.size['h']))

        self.size['w'], self.size['h'] = self.image.get_size()
        self.rect = self.image.get_rect()
        self.toggle_fullscreen()
        self.image.convert()

        # x,y: initial top left corner.
        self.x = 0
        self.y = 0

        # x1,y1: the second image will start to the left of the first
        # one, creating the illusion of infinite scrolling
        self.x1 = -self.size['w']
        self.y1 = 0
        self.x_offset = -5

    def pan(self):
        # Offset the starting points of both copies of the background:
        self.x1 += self.x_offset
        self.x += self.x_offset

        # Rollover background to the right side, depending on which
        # side we're scrolling.
        if self.x_offset <= 0:
            if self.x < -self.size['w']:
                self.x += 2*self.size['w']
            if self.x1 < -self.size['w']:
                self.x1 += 2*self.size['w']
        else:
            if self.x > self.size['w']:
                self.x = -2*self.size['w']
            if self.x1 > self.size['w']:
                self.x1 = -2*self.size['w']

        # Draw the background twice, displaced
        self.screen.blit(self.image, (self.x, self.y))
        self.screen.blit(self.image, (self.x1, self.y))
