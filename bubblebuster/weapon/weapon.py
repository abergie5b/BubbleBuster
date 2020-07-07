from bubblebuster.link import Link, LinkMan
from bubblebuster.image import ImageMan, ImageNames
from bubblebuster.timer import ClickExplodeCommand, TimerMan
from bubblebuster.group import GroupNames, GroupMan
from bubblebuster.sprite import BoxSpriteMan, BoxSpriteNames
from bubblebuster.settings import InterfaceSettings
import bubblebuster.collision as cl

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

        # collisions
        self.rect = None

        # add custom crap about the weapon
        self.duration = 0
        self.radius = 0
        self.radius_delta = 0
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 0
        self.largecost = 0

        #
        self.is_active = False

        # stats
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
        if not self.is_active:
            self.is_active = True
            # left click sprite
            self.rect = BoxSpriteMan.instance.add(BoxSpriteNames.EXPLOSION,
                                                  2,
                                                  self.radius // 2,
                                                  xcurs,
                                                  ycurs,
                                                  duration=self.duration,
                                                  delta=self.radius_delta,
                                                  color=InterfaceSettings.EXPLOSIONCOLOR
                                                  )
            self.rect.weapon = self

            # collision pairs for bubbles
            circle_group = GroupMan.instance.find(GroupNames.CIRCLE)
            cl.CollisionPairMan.instance.attach_to_group_asobja(circle_group, self.rect, cl.CollisionCirclePair)

            # start the explosion
            click_explode = ClickExplodeCommand(self.rect)
            TimerMan.instance.add(click_explode, 0)

            self.stats_usedround += self.smallcost
            self.ammo -= self.smallcost

    def rshoot(self, xcurs, ycurs):
        if not self.is_active:
            self.is_active = True
            # right click sprite
            self.rect = BoxSpriteMan.instance.add(BoxSpriteNames.EXPLOSION,
                                                  2,
                                                  self.radius*2, # height
                                                  xcurs,
                                                  ycurs,
                                                  duration=self.duration,
                                                  delta=self.radius_delta*2,
                                                  color=InterfaceSettings.EXPLOSIONCOLOR
                                                  )
            self.rect.weapon = self

            # collision pairs for bubbles
            circle_group = GroupMan.instance.find(GroupNames.CIRCLE)
            cl.CollisionPairMan.instance.attach_to_group_asobja(circle_group, self.rect, cl.CollisionCirclePair)

            # start the explosion
            click_explode = ClickExplodeCommand(self.rect)
            TimerMan.instance.add(click_explode, 0)

            self.stats_usedround += self.largecost
            self.ammo -= self.largecost


class Finger(ExplodeWeapon):
    def __init__(self, name):
        super().__init__(name)

        # image
        self.image = ImageMan.instance.find(ImageNames.FINGER)

        self.duration = 10
        self.radius = 6
        self.radius_delta = 1
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 1
        self.largecost = 2


class Thumb(ExplodeWeapon):
    def __init__(self, name):
        super().__init__(name)

        # image
        self.image = ImageMan.instance.find(ImageNames.THUMB)

        self.duration = 10
        self.radius = 12
        self.radius_delta = 2
        self.max_ammo = inf
        self.ammo = inf

        self.smallcost = 1
        self.largecost = 2


class Hand(ExplodeWeapon):
    def __init__(self, name):
        super().__init__(name)

        # image
        self.image = ImageMan.instance.find(ImageNames.HAND)

        self.duration = 10
        self.radius = 18
        self.radius_delta = 3
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



