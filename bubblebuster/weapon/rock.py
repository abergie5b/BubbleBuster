from bubblebuster.weapon import Weapon


class Rock(Weapon):
    def __init__(self, name):
        super().__init__(name)

        self.duration = 10
        self.radius = 15
        self.radius_delta = 25
        self.max_ammo = 10
        self.ammo = 10

        self.smallcost = 1
        self.largecost = 2

