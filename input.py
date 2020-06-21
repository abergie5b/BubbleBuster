from link import *
from subject import *
from gamesprite import *
from sprite import *
from timer import *

import pygame
from enum import Enum

class BUTTON(Enum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    SCROLLDOWN = 4
    SCROLLUP = 5


class InputObserver(Link):
    def __init__(self):
        raise NotImplementedError('this is a singleton class')

    def notify(self, xcurs, ycurs):
        raise NotImplementedError('this is an abstract method')


class LMouseClickCircle(InputObserver):
    def __init__(self):
        pass

    def notify(self, screen, xcurs, ycurs):
        #circle = GameSprite(SpriteNames.CIRCLE, ImageNames.CIRCLE, (1, 1), (xcurs, ycurs))
        #GameSpriteMan.add(circle)
        print('notifying left mouse click at %d %d' % (xcurs, ycurs))
        click_explode = ClickExplodeCommand(xcurs, ycurs)
        TimerMan.instance.add(click_explode, 0)

class RMouseClickCircle(InputObserver):
    def __init__(self):
        pass

    def notify(self, screen, xcurs, ycurs):
        print('notifying right mouse click at %d %d' % (xcurs, ycurs))
        click_explode = ClickExplodeCommand(xcurs, ycurs)
        TimerMan.instance.add(click_explode, 0)


class InputSubject(Subject):
    def __init__(self):
        self.objA = None
        self.objB = None
        self.head = None

    def notify(self, screen, xcurs, ycurs):
        observer = self.head
        while observer:
            observer.notify(screen, xcurs, ycurs)
            observer = observer.next


class InputMan(LinkMan):
    instance = None

    @staticmethod
    def _init(instance):
        instance.lmouse = InputSubject()
        instance.lmouse_prev = False

        instance.rmouse = InputSubject()
        instance.rmouse_prev = False

    @staticmethod
    def create():
        if not InputMan.instance:
            InputMan.instance = InputMan.__new__(InputMan)
            InputMan.instance.head = None
            InputMan._init(InputMan.instance)
        return InputMan.instance

    def update(self, game):
        event = pygame.event.poll()
        xcurs, ycurs = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == BUTTON.LEFT.value:
                self.lmouse.notify(game.screen, xcurs, ycurs)

            if event.button == BUTTON.RIGHT.value:
                self.rmouse.notify(game.screen, xcurs, ycurs)

            self.lmouse_prev = event.button == BUTTON.LEFT.value
            self.rmouse_prev = event.button == BUTTON.RIGHT.value

        if event.type == pygame.MOUSEMOTION:
            print("mouse at %d,%d" % (xcurs, ycurs))

        if event.type == pygame.QUIT:
            game.running = False

