from bubblebuster.link import Link, LinkMan
from bubblebuster.timer import TimerMan, ClickExplodeCommand
from bubblebuster.player import PlayerMan, PlayerNames
from bubblebuster.font import FontMan, FontNames
from bubblebuster.collision import intersect
from bubblebuster.settings import InterfaceSettings
from bubblebuster.settings import GameSettings
from bubblebuster.sound import SoundMan, SoundNames
import bubblebuster.scene as scene
import bubblebuster.input.subject as subject

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


class KeyPressObserver(InputObserver):
    def __init__(self, command, delta_time):
        self.command = command
        self.delta_time = delta_time

    def notify(self, screen, xcurs, ycurs):
        self.command.execute(self.delta_time)


class MouseClickObserver(InputObserver):
    def __init__(self, font, scene_change, player=None):
        self.font = font
        self.width, self.height = font.font.size(self.font.text)
        self.rectA = pygame.Rect(self.font.posx+self.width//2, 
                                 self.font.posy+self.height//2, 
                                 self.width, 
                                 self.height
        )
        self.rectB = pygame.Rect(0, 0, 1, 1)
        self.scene_change = scene_change
        self.player = player

    def notify(self, screen, xcurs, ycurs):
        self.rectB.x = xcurs
        self.rectB.y = ycurs
        if intersect(self.rectA, self.rectB):
            bubblepop = SoundMan.instance.find(SoundNames.BUBBLEPOP)
            bubblepop.play()
            scene.SceneContext.instance.set_state(self.scene_change, player=self.player)


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
            sound = SoundMan.instance.find(SoundNames.SMALLEXPLODE)
            sound.play()
            player.explosions -= GameSettings.SMALLEXPLOSIONCOST
            player.stats_explosions += GameSettings.SMALLEXPLOSIONCOST
            player.stats_explosionsround += GameSettings.SMALLEXPLOSIONCOST
            click_explode = ClickExplodeCommand(xcurs, 
                                                ycurs, 
                                                GameSettings.EXPLOSION_RADIUS//2,
                                                GameSettings.EXPLOSION_RADIUS_DELTA//2,
                                                GameSettings.EXPLOSION_MAX_LIVES//2
            )
            TimerMan.instance.add(click_explode, 0)
            font = FontMan.instance.find(FontNames.EXPLOSIONS)
            font.text = player.explosions


class RMouseClickCircleObserver(InputObserver):
    def notify(self, screen, xcurs, ycurs):
        player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
        if player and player.explosions >= GameSettings.LARGEEXPLOSIONCOST:
            sound = SoundMan.instance.find(SoundNames.LARGEEXPLODE)
            sound.play()
            player.explosions -= GameSettings.LARGEEXPLOSIONCOST
            player.stats_explosions += GameSettings.LARGEEXPLOSIONCOST
            player.stats_explosionsround += GameSettings.LARGEEXPLOSIONCOST
            click_explode = ClickExplodeCommand(xcurs, 
                                                ycurs, 
                                                GameSettings.EXPLOSION_RADIUS,
                                                GameSettings.EXPLOSION_RADIUS_DELTA,
                                                GameSettings.EXPLOSION_MAX_LIVES
            )
            TimerMan.instance.add(click_explode, 0)
            font = FontMan.instance.find(FontNames.EXPLOSIONS)
            font.text = player.explosions


class InputSubject(subject.Subject):
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

        self.keypress = InputSubject()
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
                current_scene_name = game.scene_context.scene_state.name
                if current_scene_name == scene.SceneNames.PLAY or scene.SceneNames.SCENESWITCH:
                    player = game.scene_context.scene_play.playerone
                    GameSettings.init()
                    player.reset()
                    scene.SceneContext.instance.reset()

                scene.SceneContext.instance.set_state(scene.SceneNames.MENU)

            self.keypress.notify(game.screen, xcurs, ycurs)
                

        self.mousecursor.notify(game.screen, xcurs, ycurs)

        # move dis
        if event.type == pygame.QUIT:
            game.running = False

    @staticmethod
    def set_active(manager):
        InputMan.instance = manager
