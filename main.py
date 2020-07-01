from bubblebuster.scene import SceneContext
from bubblebuster.settings import GameSettings, InterfaceSettings, DEBUG, VERSION

import pygame


class Game:
    def __init__(self):
        # required for pygame
        pygame.init()

        title = "Bubble Buster v%s" % VERSION
        if DEBUG:
            flags = pygame.RESIZABLE
            title += ' DEEEBUGGG'
        else:
            flags = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(
            (InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT),
            flags
        )
        pygame.display.set_caption(title)

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

