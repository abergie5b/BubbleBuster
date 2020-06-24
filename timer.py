from link import Link, LinkMan
from sprite import BoxSpriteMan, BoxSpriteNames
from collision import CollisionPairMan, CollisionCirclePair
from groups import GroupMan, GroupNames
from font import FontMan, FontNames
from player import PlayerMan, PlayerNames
from settings import *

import pygame
from enum import Enum

class TimeEventNames(Enum):
    CLICKEXPLODE = 1


class Command(Link):
    def __init__(self):
        raise NotImplementedError('this is a singleton class')

    def execute(self, delta_time, *args):
        raise NotImplementedError('this is an abstract method')


class DestroySpriteCommand(Command):
    def __init__(self, sprite, multiplier=1):
        self.sprite = sprite
        self.multiplier = multiplier

    def execute(self, delta_time):
        self.sprite.destroy(multiplier=self.multiplier)


class RemoveFontCommand(Command):
    def __init__(self, font):
        self.font = font

    def execute(self, delta_time):
        FontMan.instance.remove(self.font)


class ClickExplodeCommand(Command):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 2
        self.radius = EXPLOSION_RADIUS
        self.delta = EXPLOSION_RADIUS_DELTA
        self.lives = EXPLOSION_MAX_LIVES
        self.color = (255, 255, 255)
        self.rect = None
        self.circle_group = GroupMan.instance.find(GroupNames.CIRCLE)

    def execute(self, delta_time):
        if self.lives == EXPLOSION_MAX_LIVES:
            self.rect = BoxSpriteMan.instance.add(BoxSpriteNames.EXPLOSION, 
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
            BoxSpriteMan.instance.remove(self.rect)
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
    instance = None

    @staticmethod
    def create():
        if not TimerMan.instance:
            TimerMan.instance = TimerMan.__new__(TimerMan)
            TimerMan.instance.head = None
            TimerMan.instance.current_time = 0
        return TimerMan.instance

    def add(self, command, delta_time):
        event = TimeEvent(command, delta_time)
        self.base_add(event)

    def update(self, game, time):
        self.current_time = time
        head = self.head
        while head:
            next_ = head.next
            if self.current_time >= head.trigger_time:
                head.process()
                self.base_remove(head)
            head = next_

