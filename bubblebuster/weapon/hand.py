from bubblebuster.weapon import Weapon
from math import inf


class Hand(Weapon):
    def __init__(self, name):
        super().__init__(name)

        self.duration = 5
        self.radius = 15
        self.radius_delta = 15
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 1
        self.largecost = 2

