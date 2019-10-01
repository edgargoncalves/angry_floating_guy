"""asd"""


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
