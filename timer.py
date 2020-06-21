from link import *

import pygame
from enum import Enum

class TimeEventNames(Enum):
    CLICKEXPLODE = 1


class Command(Link):
    def __init__(self):
        raise NotImplementedError('this is a singleton class')

    def execute(self, delta_time, *args):
        raise NotImplementedError('this is an abstract method')


class ClickExplodeCommand(Link):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.delta = 5
        self.lives = 10
        self.radius = 10

    def execute(self, delta_time, *args):
        screen = args[0].screen
        print('drawing circle at %d %d with radius %d lives %d' % (self.x, self.y, self.radius, self.lives))
        pygame.draw.circle(screen, 
                           (255, 255, 255), 
                           (self.x, self.y), 
                           self.radius
        )
        self.radius += self.delta
        self.lives -= 1
        if self.lives:
            TimerMan.instance.add(self, delta_time)

class TimeEvent(Link):
    def __init__(self, command, delta_time):
        super().__init__()
        self.command = command
        self.delta_time = delta_time
        self.trigger_time = TimerMan.instance.current_time + delta_time

    def process(self, *args):
        self.command.execute(self.delta_time, *args)


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
                head.process(game)
                self.base_remove(head)
            head = next_

