from link import Link, LinkMan
from sprite import BoxSpriteMan, BoxSpriteNames
from collision import CollisionPairMan, CollisionCirclePair

import pygame
from enum import Enum

EXPLOSION_MAX_LIVES = 10

class TimeEventNames(Enum):
    CLICKEXPLODE = 1


class Command(Link):
    def __init__(self):
        raise NotImplementedError('this is a singleton class')

    def execute(self, delta_time, *args):
        raise NotImplementedError('this is an abstract method')


class DestroySpriteCommand(Link):
    def __init__(self, sprite):
        self.sprite = sprite

    def execute(self, delta_time):
        self.sprite.destroy()


class ClickExplodeCommand(Link):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 2
        self.radius = 10
        self.delta = 5
        self.lives = EXPLOSION_MAX_LIVES
        self.color = (255, 255, 255)
        self.rect = None

    def execute(self, delta_time):
        #print('updating circle at %d %d with radius %d lives %d' % (self.x, self.y, self.radius, self.lives))
        if self.lives == EXPLOSION_MAX_LIVES:
            self.rect = BoxSpriteMan.instance.add(BoxSpriteNames.EXPLOSION, 
                                                  self.width, 
                                                  self.radius*2, 
                                                  self.x, 
                                                  self.y, 
                                                  color=self.color
            )
            # todo - bind self.rect to a circle group
            self.collision_pairA = CollisionCirclePair(self.rect, BoxSpriteMan.instance.find(BoxSpriteNames.CIRCLEA))
            self.collision_pairB = CollisionCirclePair(self.rect, BoxSpriteMan.instance.find(BoxSpriteNames.CIRCLEB))
            self.collision_pairC = CollisionCirclePair(self.rect, BoxSpriteMan.instance.find(BoxSpriteNames.CIRCLEC))
            self.collision_pairD = CollisionCirclePair(self.rect, BoxSpriteMan.instance.find(BoxSpriteNames.CIRCLED))
            self.collision_pairE = CollisionCirclePair(self.rect, BoxSpriteMan.instance.find(BoxSpriteNames.CIRCLEE))

            CollisionPairMan.instance.add(self.collision_pairA)
            CollisionPairMan.instance.add(self.collision_pairB)
            CollisionPairMan.instance.add(self.collision_pairC)
            CollisionPairMan.instance.add(self.collision_pairD)
            CollisionPairMan.instance.add(self.collision_pairE)

        self.rect.radius = self.radius = self.radius + self.delta
        self.rect.height = self.radius*2
        self.lives -= 1

        if self.lives:
            TimerMan.instance.add(self, delta_time)
        else:
            BoxSpriteMan.instance.remove(self.rect)
            CollisionPairMan.instance.remove(self.rect)


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

