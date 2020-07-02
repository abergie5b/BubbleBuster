from bubblebuster.link import LinkMan
from bubblebuster.settings import GameSettings
from bubblebuster.input import InputSubject, Simulation
import bubblebuster.scene as scene
from bubblebuster.player import PlayerMan, PlayerNames

import pygame
from enum import Enum

class BUTTON(Enum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    SCROLLDOWN = 4
    SCROLLUP = 5


class InputMan(LinkMan):
    instance = None
    def __init__(self):
        super().__init__()
        self.lmouse = InputSubject()
        self.lmouse_prev = False

        self.rmouse = InputSubject()
        self.rmouse_prev = False

        self.keypress = InputSubject()
        self.mousecursor = InputSubject()
        InputMan.instance = self

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
                player = PlayerMan.instance.find(PlayerNames.PLAYERONE)
                if player:
                    player.reset()
                if current_scene_name != scene.SceneNames.SETTINGS:
                    GameSettings.init()
                scene.SceneContext.instance.reset(player=player)
                scene.SceneContext.instance.set_state(scene.SceneNames.MENU, player=player)

            # delete me for "production" builds
            Simulation.instance.update(event)

            self.keypress.notify(game.screen, xcurs, ycurs)
                
        self.mousecursor.notify(game.screen, xcurs, ycurs)

        # move dis
        if event.type == pygame.QUIT:
            game.running = False

    @staticmethod
    def set_active(manager):
        InputMan.instance = manager
