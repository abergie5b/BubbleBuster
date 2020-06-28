from bubblebuster.link import Link, LinkMan

from enum import Enum

class WeaponNames(Enum):
    FINGER = 1


class Weapon(Link):
    def __init__(self, name):
        super().__init__()
        self.name = name
        # add inputs
        # add more custom crap about the weapon

class Finger(Weapon):
    def __init__(self, name):
        super().__init__(name)


class Thumb(Weapon):
    def __init__(self, name):
        super().__init__(name)


class Hand(Weapon):
    def __init__(self, name):
        super().__init__(name)


class Pebble(Weapon):
    def __init__(self, name):
        super().__init__(name)


class Rock(Weapon):
    def __init__(self, name):
        super().__init__(name)


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



