from bubblebuster.link import Link, LinkMan
from bubblebuster.image import ImageMan, ImageNames

from math import inf
from enum import Enum

class WeaponNames(Enum):
    FINGER = 1
    THUMB = 2
    HAND = 3
    PEBBLE = 4
    ROCK = 5


class Weapon(Link):
    def __init__(self, name):
        super().__init__()
        self.name = name
        # add inputs

        # image
        self.image = ImageMan.instance.find(ImageNames.TESTMOUSE)

        # add more custom crap about the weapon
        self.duration = 0
        self.radius = 0
        self.radius_delta = 0
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 0
        self.largecost = 0


class Finger(Weapon):
    def __init__(self, name):
        super().__init__(name)

        self.duration = 25
        self.radius = 10
        self.radius_delta = 5
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 1
        self.largecost = 2


class Thumb(Weapon):
    def __init__(self, name):
        super().__init__(name)

        self.duration = 30
        self.radius = 15
        self.radius_delta = 5
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 1
        self.largecost = 2


class Hand(Weapon):
    def __init__(self, name):
        super().__init__(name)

        self.duration = 35
        self.radius = 20
        self.radius_delta = 5
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 1
        self.largecost = 2


class Pebble(Weapon):
    def __init__(self, name):
        super().__init__(name)

        self.duration = 40
        self.radius = 5
        self.radius_delta = 25
        self.max_ammo = 10
        self.ammo = 10

        self.smallcost = 1
        self.largecost = 2


class Rock(Weapon):
    def __init__(self, name):
        super().__init__(name)

        self.duration = 50
        self.radius = 15
        self.radius_delta = 30
        self.max_ammo = 10
        self.ammo = 10

        self.smallcost = 1
        self.largecost = 2


class WeaponMan(LinkMan):
    def compare(self, a, b):
        return a.name == b

    def add(self, name, data):
        image = Weapon(name, data)
        self.base_add(image)

    def find(self, image):
        return self.base_find(image)

    @staticmethod
    def set_active(manager):
        WeaponMan.instance = manager



