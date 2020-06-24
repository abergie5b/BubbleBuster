from link import Link, LinkMan
from subject import Subject
from timer import TimerMan, ClickExplodeCommand, ClickMiniExplodeCommand
from player import PlayerMan, PlayerNames
from font import FontMan, FontNames
from collision import intersect
from settings import InterfaceSettings
import scene
from settings import GameSettings

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
        pass

    def notify(self, screen, xcurs, ycurs):
        raise NotImplementedError('this is an abstract method')


class MouseClickObserver(InputObserver):
    def __init__(self, font, scene_change):
        self.font = font
        self.width, self.height = font.font.size(self.font.text)
        self.rectA = pygame.Rect(self.font.posx+self.width//2, 
                                 self.font.posy+self.height//2, 
                                 self.width, 
                                 self.height
        )
        self.rectB = pygame.Rect(0, 0, 1, 1)
        self.scene_change = scene_change

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if intersect(self.rectA, self.rectB):
            scene.SceneContext.instance.set_state(self.scene_change)


class MouseClickExitObserver(MouseClickObserver):
    def __init__(self, font, scene):
        super().__init__(font, scene)

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if intersect(self.rectA, self.rectB):
            # handle this
            scene.SceneContext.instance.game.running = False


class MouseHoverHighlightObserver(MouseClickObserver):
    def __init__(self, font, scene):
        super().__init__(font, scene)

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if intersect(self.rectA, self.rectB):
            self.font.color = InterfaceSettings.MOUSEHIGHLIGHTFONTCOLOR
        else:
            self.font.color = InterfaceSettings.FONTCOLOR


class LMouseClickCircleObserver(InputObserver):
    def notify(self, screen, xcurs, ycurs):
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        if player and player.explosions >= GameSettings.SMALLEXPLOSIONCOST:
            player.explosions -= GameSettings.SMALLEXPLOSIONCOST
            click_explode = ClickMiniExplodeCommand(xcurs, ycurs)
            TimerMan.instance.add(click_explode, 0)
            font = FontMan.instance.find(FontNames.EXPLOSIONS)
            font.text = player.explosions


class RMouseClickCircleObserver(InputObserver):
    def notify(self, screen, xcurs, ycurs):
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        if player and player.explosions >= GameSettings.LARGEEXPLOSIONCOST:
            player.explosions -= GameSettings.LARGEEXPLOSIONCOST
            click_explode = ClickExplodeCommand(xcurs, ycurs)
            TimerMan.instance.add(click_explode, 0)
            font = FontMan.instance.find(FontNames.EXPLOSIONS)
            font.text = player.explosions


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
    def __init__(self):
        super().__init__()
        self.lmouse = InputSubject()
        self.lmouse_prev = False

        self.rmouse = InputSubject()
        self.rmouse_prev = False

        self.mousecursor = InputSubject()

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

        self.mousecursor.notify(game.screen, xcurs, ycurs)

        # move dis
        if event.type == pygame.QUIT:
            game.running = False

    @staticmethod
    def set_active(manager):
        InputMan.instance = manager
