from bubblebuster.link import Link, LinkMan
from bubblebuster.image import ImageMan, ImageNames
from bubblebuster.timer import ClickExplodeCommand, TimerMan
from bubblebuster.groups import GroupNames, GroupMan
from bubblebuster.sprite import BoxSpriteMan, BoxSpriteNames
from bubblebuster.settings import InterfaceSettings

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

        # add custom crap about the weapon
        self.duration = 0
        self.radius = 0
        self.radius_delta = 0
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 0
        self.largecost = 0

        self.stats_usedtotal = 0
        self.stats_usedround = 0
        self.stats_usedroundprev = 0

    def reset(self):
        self.ammo = self.max_ammo
        self.stats_usedroundprev = self.stats_usedround
        self.stats_usedtotal += self.stats_usedround
        self.stats_usedround = 0


class ExplodeWeapon(Weapon):
    def __init__(self, name):
        super().__init__(name)

    def lshoot(self, xcurs, ycurs):
        self.rectx = xcurs
        self.recty = ycurs
        click_explode = ClickExplodeCommand(self.rect)
        TimerMan.instance.add(click_explode, 0)
        self.stats_usedround += self.smallcost
        self.ammo -= self.smallcost

    def rshoot(self, xcurs, ycurs):
        self.bigrectx = xcurs
        self.bigrecty = ycurs
        click_explode = ClickExplodeCommand(self.bigrect)
        TimerMan.instance.add(click_explode, 0)
        self.stats_usedround += self.largecost
        self.ammo -= self.largecost


class Finger(ExplodeWeapon):
    def __init__(self, name):
        super().__init__(name)

        # image
        self.image = ImageMan.instance.find(ImageNames.FINGER)

        self.duration = 25
        self.radius = 10
        self.radius_delta = 5
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 1
        self.largecost = 2

        # left click sprite
        self.rectw = 2
        self.rectr = self.radius // 2
        self.rectx = -100
        self.recty = -100
        self.rect = BoxSpriteMan.instance.add(BoxSpriteNames.EXPLOSION,
                                              self.width // 2,
                                              self.radius // 2,
                                              self.rectx,
                                              self.recty,
                                              color=InterfaceSettings.EXPLOSIONCOLOR
                                              )
        # !!!!!!!!!!!!!!!
        self.rect.delta = self.radius_delta

        # right click sprite
        self.bigrectw = 2
        self.bigrectr = self.radius
        self.bigrectx = -100
        self.bigrecty = -100
        self.bigrect = BoxSpriteMan.instance.add(BoxSpriteNames.EXPLOSION,
                                              self.width,
                                              self.radius*2, # height
                                              self.rectx,
                                              self.recty,
                                              color=InterfaceSettings.EXPLOSIONCOLOR
                                              )
        # !!!!!!!!!!!!!!!
        self.rect.delta = self.radius_delta

        # add these to circle group
        circle_group = GroupMan.instance.find(GroupNames.CIRCLE)
        circle_group.add(self.rect)
        circle_group.add(self.bigrect)


class Thumb(ExplodeWeapon):
    def __init__(self, name):
        super().__init__(name)

        # image
        self.image = ImageMan.instance.find(ImageNames.THUMB)

        self.duration = 30
        self.radius = 15
        self.radius_delta = 5
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 1
        self.largecost = 2


class Hand(ExplodeWeapon):
    def __init__(self, name):
        super().__init__(name)

        # image
        self.image = ImageMan.instance.find(ImageNames.HAND)

        self.duration = 35
        self.radius = 20
        self.radius_delta = 5
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 1
        self.largecost = 2


class Pebble(ExplodeWeapon):
    def __init__(self, name):
        super().__init__(name)

        self.duration = 40
        self.radius = 5
        self.radius_delta = 25
        self.max_ammo = 10
        self.ammo = 10

        self.smallcost = 1
        self.largecost = 2


class Rock(ExplodeWeapon):
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



