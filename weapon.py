from link import Link, LinkMan

from enum import Enum

class WeaponNames(Enum):
    FINGER = 1


class Weapon(Link):
    def __init__(self, name, player):
        super().__init__()
        self.name = name
        self.player = player


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



