from link import Link, LinkMan
from subject import Subject
from timer import TimerMan, ClickExplodeCommand
from player import PlayerMan, PlayerNames
from font import FontMan, FontNames
from collision import intersect
from settings import InterfaceSettings
import scene
from settings import GameSettings
from sound import SoundMan, SoundNames

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


class MouseClickSettingsObserver(InputObserver):
    def __init__(self, font, setting, font_name, increment):
        self.font = font
        self.width, self.height = font.font.size(self.font.text)
        self.rectA = pygame.Rect(self.font.posx+self.width//2, 
                                 self.font.posy+self.height//2, 
                                 self.width, 
                                 self.height
        )
        self.rectB = pygame.Rect(0, 0, 1, 1)
        self.setting = setting
        self.font_name = font_name
        self.increment = increment

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if intersect(self.rectA, self.rectB):
            value = getattr(GameSettings, self.setting)
            if value + self.increment >= 0: # nice try
                setattr(GameSettings, self.setting, value + self.increment)
                # not ideal to do like this
                value = getattr(GameSettings, self.setting)
                font = FontMan.instance.find(self.font_name)
                font.text = str(value)


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
            bubblepop = SoundMan.instance.find(SoundNames.BUBBLEPOP)
            bubblepop.play()
            scene.SceneContext.instance.set_state(self.scene_change)


class MouseClickExitObserver(MouseClickObserver):
    def __init__(self, font, scene):
        super().__init__(font, scene)

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if intersect(self.rectA, self.rectB):
            # handle this somewhere else please
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
            click_explode = ClickExplodeCommand(xcurs, 
                                                ycurs, 
                                                GameSettings.EXPLOSION_RADIUS//2,
                                                GameSettings.EXPLOSION_RADIUS_DELTA//2,
                                                GameSettings.EXPLOSION_MAX_LIVES//2
            )
            TimerMan.instance.add(click_explode, 0)
            font = FontMan.instance.find(FontNames.EXPLOSIONS)
            font.text = player.explosions
            sound = SoundMan.instance.find(SoundNames.SMALLEXPLODE)
            sound.play()


class RMouseClickCircleObserver(InputObserver):
    def notify(self, screen, xcurs, ycurs):
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        if player and player.explosions >= GameSettings.LARGEEXPLOSIONCOST:
            player.explosions -= GameSettings.LARGEEXPLOSIONCOST
            click_explode = ClickExplodeCommand(xcurs, 
                                                ycurs, 
                                                GameSettings.EXPLOSION_RADIUS,
                                                GameSettings.EXPLOSION_RADIUS_DELTA,
                                                GameSettings.EXPLOSION_MAX_LIVES
            )
            TimerMan.instance.add(click_explode, 0)
            font = FontMan.instance.find(FontNames.EXPLOSIONS)
            font.text = player.explosions
            sound = SoundMan.instance.find(SoundNames.LARGEEXPLODE)
            sound.play()


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

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                scene.SceneContext.instance.set_state(scene.SceneNames.MENU)

        self.mousecursor.notify(game.screen, xcurs, ycurs)

        # move dis
        if event.type == pygame.QUIT:
            game.running = False

    @staticmethod
    def set_active(manager):
        InputMan.instance = manager
