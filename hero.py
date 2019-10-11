"""asd"""

from drawable_item import DrawableItem


class Hero(DrawableItem):
    """Hero is an emoji that moves with arrows"""

    def __init__(self, world, boundaries):
        super(Hero, self).__init__('emoji.png', boundaries)
        self.world = world
        self.screen = None
        self.bounced = False
        self.score = 0

    def move(self):
        acceleration = self.world.acceleration
        resistance = self.world.resistance
        propulsors = self.world.propulsors

        # We want to use the instance's variables as the previous (ini) state
        velocity = self.velocity.copy()
        position = self.position.copy()

        # Keyboard acceleration / braking - propulsors
        for propulsor_direction, ways in propulsors.items():
            for way, increment in ways.items():
                if self.moving[way]:
                    velocity[propulsor_direction] += increment

        hero_size = {'hori': self.size['w'], 'vert': self.size['h']}
        self.bounced = False

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
            min_edge = self.boundaries[direction][0]
            max_edge = self.boundaries[direction][1] - \
                hero_size[direction]
            p_curr = min(max(p_curr, min_edge), max_edge)
            position[direction] = p_curr

            # Make it bounce:
            if (p_ini > min_edge and p_curr == min_edge) or \
                    (p_ini < max_edge and p_curr == max_edge):
                velocity[direction] *= -1
                # Play bouncing sound effect:
                self.bounced = abs(velocity[direction]) > 1

            # Set velocity to 0 once it halts on an edge.
            if (p_ini == 0 == p_curr) or (p_ini == max_edge == p_curr):
                velocity[direction] = 0

        # Set the position and velocity for the next iteration:
        self.position = position
        self.velocity = velocity
