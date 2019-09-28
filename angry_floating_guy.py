"""Angry Floaring guy PiGame"""

import pygame
from pygame.locals import *


class World():
    """Contains details about the physics of a worl"""
    name = 'Unknown planet'
    acceleration = {}
    resistance = {}
    propulsors = {}

    def __init__(self, name, acceleration, resistance, propulsors):
        self.name = name
        self.acceleration = acceleration
        self.resistance = resistance
        self.propulsors = propulsors

    def move_object(self, obj, forces):
        """TODO: update an object's properties after moving in this world"""

    def shake(self):
        """TODO: do something interesting"""


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
    image = None
    background = None
    screen = None
    effect = None
    hero_is_moving = {}
    worlds = (EARTH, MOON, JUPITER)

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.boundaries = {'hori': [0, self.weight-50],
                           'vert': [0, self.height-50]}
        self.position = {'hori': 0, 'vert': 0}
        self.velocity = {'hori': 0, 'vert': 0}
        self.bodymass = 1       # How heavy will the object feel

        # Select a world (EARTH, JUPITER, MOON):
        self.current_world = self.worlds[0]

        self.hero_is_moving = {pygame.K_DOWN: False,
                               pygame.K_UP: False,
                               pygame.K_LEFT: False,
                               pygame.K_RIGHT: False}

        self.panning_bg = {'image': None, 'size': (0, 0), 'rect': None,
                           'screen': None, 'w': 0, 'h': 0, 'x': 0,
                           'y': 0, 'x1': 0, 'y1': 0, 'x_offset': 0}

        self.the_clock = pygame.time.Clock()

    def on_init(self):
        """Loads up variables for the game to start"""
        pygame.init()
        # frequency, size, channels, buffersize
        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        # self._display_surf = pygame.display.set_mode(
        #     self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.image = pygame.transform.scale(
            pygame.image.load("images/emoji.png"), (50, 50))
        
        self.enemy = pygame.transform.scale(
            pygame.image.load("images/batwing.png"), (50, 50))

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
        pygame.display.set_caption(
            'Angry Floating Guy! World: {} (w to change world, arrows to move, Esc to quit).'.format(self.current_world.name))

        self._running = True

    def on_event(self, event):
        """Check for key pressed events"""
        arrows = self.hero_is_moving.keys()

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
            self.hero_is_moving[event.key] = True

        elif event.type == pygame.KEYUP:
            self.hero_is_moving[event.key] = False

    def on_loop(self):
        """Handles the physics for the hero's movement."""

        acceleration = self.current_world.acceleration
        resistance = self.current_world.resistance
        propulsors = self.current_world.propulsors

        # We want to use the instance's variables as the previous (ini) state
        velocity = self.velocity.copy()
        position = self.position.copy()

        # Keyboard acceleration / braking - propulsors
        for propulsor_direction, ways in propulsors.items():
            for way, increment in ways.items():
                if self.hero_is_moving[way]:
                    velocity[propulsor_direction] += increment

        for direction in ['hori', 'vert']:
            # Inertia / resistive forces
            #    v = v0 + resistance
            # Note: resistance is opposite to velocity in sign
            if velocity[direction] != 0:
                sign = velocity[direction] / abs(velocity[direction])
                velocity[direction] -= sign * resistance[direction]

            # Acceleration components:
            # - Gravity : 9.8 m/s per time iteration, vertically, down
            # - Arrow keys (propulsors)
            # v = v0 + a*t
            velocity[direction] += acceleration[direction]

            # Displacement is based on previous position
            # Note: y axis is inverted on the screen.
            # p = p0 + v0*t + 0.5*a*t^2 = p0 + v0 + 0.5a

            # We're faking the physics laws by using the
            # accelleration-affected velocity instead of v0 plus 0.5a.
            # Note: setting some variables for this direction, easier to read
            p_ini = self.position[direction]
            p_curr = p_ini + velocity[direction]

            # Ensure final position is within screen:
            min_edge, max_edge = self.boundaries[direction]
            p_curr = min(max(p_curr, min_edge), max_edge)
            position[direction] = p_curr

            # Make it bounce:
            if (p_ini > min_edge and p_curr == min_edge) or \
                    (p_ini < max_edge and p_curr == max_edge):
                velocity[direction] *= -1
                # Play bouncing sound effect:
                if abs(velocity[direction]) > 1:
                    self.effect.play()

            # Set velocity to 0 once it halts on an edge.
            if (p_ini == 0 == p_curr) or (p_ini == max_edge == p_curr):
                velocity[direction] = 0

        # Set the position and velocity for the next iteration:
        self.position = position
        self.velocity = velocity

        # Debug message
        # print("Vertically at {:5}, ini at {:5}, vel {:5}".format(
        #     position['vert'], self.position['vert'],
        #     round(velocity['vert'], 2)))

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
        self.screen.blit(
            self.image, (self.position['hori'], self.position['vert']))
        
        self.screen.blit(
            self.enemy, (self.position['hori']+100, self.position['vert']+100))

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
