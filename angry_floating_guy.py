"""Angry Floaring guy PiGame"""

import pygame
from pygame.locals import *
from world import World
from hero import Hero
from enemy import Enemy


MOON = World('Moon',
             acceleration={'hori': 0.0, 'vert': 1.62},
             resistance={'hori': 0.5, 'vert': 0.5},
             propulsors={'hori': {pygame.K_LEFT: -1, pygame.K_RIGHT: 1},
                         'vert': {pygame.K_DOWN: 5, pygame.K_UP: -5}})
EARTH = World('Earth',
              acceleration={'hori': 0.0, 'vert': 9.8},
              resistance={'hori': 1, 'vert': 1},
              propulsors={'hori': {pygame.K_LEFT: -2, pygame.K_RIGHT: 2},
                          'vert': {pygame.K_DOWN: 12, pygame.K_UP: -14}})
JUPITER = World('Jupiter',
                acceleration={'hori': 0.0, 'vert': 24.79},
                resistance={'hori': 1.5, 'vert': 1.5},
                propulsors={'hori': {pygame.K_LEFT: -2, pygame.K_RIGHT: 2},
                            'vert': {pygame.K_DOWN: 10, pygame.K_UP: -27}})


class App:
    """Class used by PiGame"""
    background = None
    screen = None
    effect = None
    worlds = (EARTH, MOON, JUPITER)

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.boundaries = {'hori': [0, self.weight-50],
                           'vert': [0, self.height-50]}

        # Select a world (EARTH, JUPITER, MOON):
        self.current_world = self.worlds[0]

        # self.hero = DrawableItem('emoji.png')
        self.hero = Hero(self.current_world, self.boundaries)
        self.enemy = Enemy(self.hero, self.boundaries)

        self.panning_bg = {'image': None, 'size': (0, 0), 'rect': None,
                           'screen': None, 'w': 0, 'h': 0, 'x': 0,
                           'y': 0, 'x1': 0, 'y1': 0, 'x_offset': 0}

    def on_init(self):
        """Loads up variables for the game to start"""
        pygame.init()
        # frequency, size, channels, buffersize
        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        # self._display_surf = pygame.display.set_mode(
        #     self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.hero.load_from_file()
        self.enemy.load_from_file()

        # Background. Load image, and setup variables for scrolling it
        background = pygame.transform.scale(
            pygame.image.load('images/background.png'),
            (self.weight, self.height))

        self.panning_bg['image'] = background
        self.panning_bg['size'] = background.get_size()
        self.panning_bg['rect'] = background.get_rect()
        self.panning_bg['screen'] = pygame.display.set_mode(
            self.panning_bg['size'], pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.panning_bg['w'], self.panning_bg['h'] = self.panning_bg['size']
        # x,y: initial top left corner.
        self.panning_bg['x'] = 0
        self.panning_bg['y'] = 0

        # x1,y1: the second image will start to the left of the first
        # one, creating the illusion of infinite scrolling
        self.panning_bg['x1'] = -self.panning_bg['w']
        self.panning_bg['y1'] = 0
        self.panning_bg['x_offset'] = -5

        # Some music and sound fx
        self.effect = pygame.mixer.Sound('sounds/bounce.wav')
        pygame.mixer.music.load('sounds/music.wav')
        pygame.mixer.music.play(-1)

        self.screen = self.panning_bg['screen']
        self.hero.screen = self.screen
        self.enemy.screen = self.screen
        pygame.display.set_caption(
            'Angry Floating Guy! World: {} (w to change world, arrows to move, Esc to quit).'.format(self.current_world.name))

        self._running = True

    def on_event(self, event):
        """Check for key pressed events"""
        arrows = self.hero.moving.keys()

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                         (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
            self._running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            curr_world_index = self.worlds.index(self.current_world)
            next_index = (curr_world_index + 1) % 3
            self.current_world = self.worlds[next_index]
            pygame.display.set_caption(
                'Angry Floating Guy! World: {} (w to change world, arrows to move, Esc to quit).'.format(self.current_world.name))

        elif event.type == pygame.KEYDOWN and event.key in arrows:
            self.hero.moving[event.key] = True

        elif event.type == pygame.KEYUP:
            self.hero.moving[event.key] = False

    def on_loop(self):
        """Handles the physics for the hero's movement."""

        self.hero.world = self.current_world

        self.hero.move()
        if self.hero.bounced:
            self.effect.play()

        self.enemy.move()

    def on_render(self):
        # Render the background

        # Offset the starting points of both copies of the background:
        self.panning_bg['x1'] += self.panning_bg['x_offset']
        self.panning_bg['x'] += self.panning_bg['x_offset']

        # Draw the two backgrounds
        self.screen.blit(self.panning_bg['image'],
                         (self.panning_bg['x'], self.panning_bg['y']))
        self.screen.blit(self.panning_bg['image'],
                         (self.panning_bg['x1'], self.panning_bg['y1']))

        # Rollover background to the right side, depending on which
        # side we're scrolling.
        if self.panning_bg['x_offset'] <= 0:
            if self.panning_bg['x'] < -self.panning_bg['w']:
                self.panning_bg['x'] = self.panning_bg['w']
            if self.panning_bg['x1'] < -self.panning_bg['w']:
                self.panning_bg['x1'] = self.panning_bg['w']
        else:
            if self.panning_bg['x'] > self.panning_bg['w']:
                self.panning_bg['x'] = -self.panning_bg['w']
            if self.panning_bg['x1'] > self.panning_bg['w']:
                self.panning_bg['x1'] = -self.panning_bg['w']

        # now blit the hero on screen
        self.hero.blit()
        self.enemy.blit()

        # and update the screen (don't forget that!)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()

# If running interactively, you will need to run this!
# theApp = App()
# theApp.on_execute()
