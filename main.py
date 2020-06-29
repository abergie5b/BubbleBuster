import pygame

from bubblebuster.scene import SceneContext
from bubblebuster.settings import GameSettings, InterfaceSettings, DEBUG, VERSION

import ctypes
import os


class Game:
    def __init__(self):
        # required for pygame
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        ctypes.windll.user32.SetProcessDPIAware()
        self.resolution = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
        if DEBUG:
            print('detected screen resolution of %d width %d height' % (self.resolution))
        self.screen = pygame.display.set_mode((InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Bubble Buster v%s" % VERSION)

        self.running = True
        self.FPS = 90

        InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT = self.screen.get_size()
        if DEBUG:
            print('created display surface with %d width %d height' % (InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT))

        GameSettings.init()
        self.scene_context = SceneContext(self)

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

