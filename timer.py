from link import Link, LinkMan
import sprite as sp
from collision import CollisionPairMan, CollisionCirclePair
from groups import GroupMan, GroupNames
from font import FontMan, FontNames
from player import PlayerMan, PlayerNames
from settings import GameSettings
import scene

import pygame
from enum import Enum

class TimeEventNames(Enum):
    CLICKEXPLODE = 1
    FADEOUTTOAST = 2
    DESTROYSPRITE = 3
    MINICLICKEXPLODE = 4
    REMOVEFONT = 5
    SWITCHSCENE = 6

class Command(Link):
    def __init__(self):
        raise NotImplementedError('this is a singleton class')

    def execute(self, delta_time, *args):
        raise NotImplementedError('this is an abstract method')


class SwitchSceneCommand(Command):
    def __init__(self, destination, player=None):
        self.name = TimeEventNames.SWITCHSCENE
        self.destination = destination
        self.player = player

    def execute(self, delta_time):
        scene.SceneContext.instance.set_state(self.destination, player=self.player)


class DestroySpriteCommand(Command):
    def __init__(self, sprite, explosion=None):
        self.sprite = sprite
        self.explosion = explosion
        self.name = TimeEventNames.DESTROYSPRITE

    def execute(self, delta_time):
        multiplier = self.explosion.multiplier if self.explosion else 1
        self.sprite.destroy(explosion=self.explosion)


class FadeOutFontCommand(Command):
    def __init__(self, font, original_color):
        self.font = font
        self.original_color = original_color
        self.name = TimeEventNames.FADEOUTTOAST

    def execute(self, delta_time):
        r = self.font.color[0]
        g = self.font.color[1]
        b = self.font.color[2]
        r = r - 1 if r else r
        g = g - 1 if g else g
        b = b - 1 if b else b
        self.font.color = (r, g, b)
        if r or g or b:
            TimerMan.instance.add(self, 1)
        else:
            self.font.color = self.original_color
            self.font.text = ''


class RemoveFontCommand(Command):
    def __init__(self, font):
        self.font = font
        self.name = TimeEventNames.REMOVEFONT

    def execute(self, delta_time):
        FontMan.instance.remove(self.font)


class ClickExplodeCommand(Command):
    def __init__(self, x, y, radius, radius_delta, lives):
        self.x = x
        self.y = y
        self.width = 2
        self.radius = radius
        self.delta = radius_delta
        self.original_lives = lives
        self.lives = lives
        self.color = (255, 255, 255)
        self.rect = None
        self.circle_group = GroupMan.instance.find(GroupNames.CIRCLE)
        self.name = TimeEventNames.CLICKEXPLODE

    def execute(self, delta_time):
        if self.lives == self.original_lives:
            self.rect = sp.BoxSpriteMan.instance.add(sp.BoxSpriteNames.EXPLOSION, 
                                                  self.width, 
                                                  self.radius*2, 
                                                  self.x, 
                                                  self.y, 
                                                  color=self.color
            )
            self.circle_group.add(self.rect)

        self.rect.radius = self.radius = self.radius + self.delta
        self.rect.height = self.radius*2
        self.lives -= 1

        if self.lives:
            TimerMan.instance.add(self, delta_time)
        else:
            sp.BoxSpriteMan.instance.remove(self.rect)
            CollisionPairMan.instance.remove(self.rect)
            node = self.circle_group.find(self.rect)
            self.circle_group.remove(node)


class TimeEvent(Link):
    def __init__(self, command, delta_time):
        super().__init__()
        self.command = command
        self.delta_time = delta_time
        self.trigger_time = TimerMan.instance.current_time + delta_time

    def process(self):
        self.command.execute(self.delta_time)


class TimerMan(LinkMan):
    def __init__(self):
        super().__init__()
        self.head = None
        self.current_time = 0

    def add(self, command, delta_time):
        event = TimeEvent(command, delta_time)
        self.base_add(event)

    def compare(self, a, b):
        return a.command.name == b

    def find(self, command):
        return self.base_find(command)

    def remove(self, command):
        self.base_remove(command)

    def update(self, game, time):
        self.current_time = time
        head = self.head
        while head:
            next_ = head.next
            if self.current_time >= head.trigger_time:
                head.process()
                self.base_remove(head)
            head = next_

    @staticmethod
    def set_active(manager):
        TimerMan.instance = manager

