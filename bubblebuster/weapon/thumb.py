from bubblebuster.weapon import Weapon
from math import inf


class Thumb(Weapon):
    def __init__(self, name):
        super().__init__(name)

        self.duration = 5
        self.radius = 10
        self.radius_delta = 10
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 1
        self.largecost = 2

