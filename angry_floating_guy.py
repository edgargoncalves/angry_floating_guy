"""Angry Floaring guy PiGame"""

import pdb
import pygame
from pygame.locals import *
from world import World
from hero import Hero
from enemy import Enemy
from background import Background


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
    effect = None
    worlds = (EARTH, MOON, JUPITER)

    def __init__(self):
        self._running = True
        self.clock = None

        # Select a world (EARTH, JUPITER, MOON):
        self.current_world = self.worlds[0]

        self.background = Background(640, 400)
        self.hero = Hero(self.current_world, self.background.boundaries)
        self.enemy = Enemy(self.hero, self.background)

    def on_init(self):
        """Loads up variables for the game to start"""
        pygame.init()
        self.background.load_from_file()
        self.hero.load_from_file()
        self.enemy.load_from_file()

        # Some music and sound fx
        # frequency, size, channels, buffersize
        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.effect = pygame.mixer.Sound('sounds/bounce.wav')
        pygame.mixer.music.load('sounds/music.wav')
        pygame.mixer.music.play(-1)

        self.hero.screen = self.background.screen
        self.enemy.screen = self.background.screen
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(
            'Angry Floating Guy! World: {} (w to change world, arrows to move, Esc to quit).'.format(self.current_world.name))

        self._running = True

    def on_event(self, event):
        """Check for key pressed events"""
        arrows = self.hero.moving.keys()

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                         (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
            self._running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            self.background.toggle_fullscreen()
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
        self.clock.tick(self.background.fps)
        self.hero.world = self.current_world

        if self.hero.is_colliding_with(self.enemy):
            self.hero.score += 1

        self.hero.move()
        if self.hero.bounced:
            self.effect.play()

        self.enemy.move()

    def on_render(self):
        # Render the background
        self.background.pan()

        # Show the hero's score
        smallfont = pygame.font.SysFont("comicsansms", 25)
        text = smallfont.render(
            "Score: "+str(self.hero.score), True, (255, 0, 0))
        self.background.screen.blit(text, [0, 0])

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
