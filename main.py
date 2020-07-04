import bubblebuster.scene.scenecontext as sccxt
from bubblebuster.settings import GameSettings, InterfaceSettings, DEBUG, VERSION

import pygame


class Game:
    def __init__(self):
        # required for pygame
        pygame.init()

        title = "Bubble Buster v%s" % VERSION
        if DEBUG:
            flags = pygame.RESIZABLE
            title += ' DEBUG'
        else:
            flags = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(
            (InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT),
            flags
        )
        pygame.display.set_caption(title)

        self.running = True
        self.FPS = 90

        if not InterfaceSettings.DARKMODE:
            InterfaceSettings.BACKGROUND_COLOR = InterfaceSettings.BACKGROUND_COLOR_LIGHT
            InterfaceSettings.MOUSEHIGHLIGHTFONTCOLOR = InterfaceSettings.MOUSEHIGHLIGHTFONTCOLOR_LIGHT
            InterfaceSettings.FONTITLECOLOR = InterfaceSettings.FONTTITLECOLOR_LIGHT
            InterfaceSettings.FONTCOLOR = InterfaceSettings.FONTCOLOR_LIGHT

        InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT = self.screen.get_size()
        if DEBUG:
            print('created display surface with %d width %d height' % (InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT))

        GameSettings.init()
        self.scene_context = sccxt.SceneContext(self)

    def draw(self):
        self.scene_context.scene_state.draw()

        # draw the entire screen
        pygame.display.update()

        # clear the display
        # is there ... a better way? -.-
        self.screen.fill(InterfaceSettings.BACKGROUND_COLOR)

    def update(self):
        self.scene_context.scene_state.update()

    def run(self):

        # Fill the background with black
        self.scene_context.scene_state.screen.fill(InterfaceSettings.BACKGROUND_COLOR)

        # get clock for FPS
        clock = pygame.time.Clock()

        # main event loop
        while self.running:

            # update objects
            self.update()

            # draw objects
            self.draw()

            # tick tock
            clock.tick(self.FPS)

        # quit
        pygame.quit()


if __name__ == '__main__':
    Game().run()

