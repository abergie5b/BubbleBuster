import pygame

from input import *
from image import *
from sprite import *
from gamesprite import *


class Game:
    def __init__(self):
        self.image_manager = ImageMan.create()
        self.sprite_manager = SpriteMan.create()
        self.gamesprite_manager = GameSpriteMan()
        self.boxsprite_manager = BoxSpriteMan.create()
        self.input_manager = InputMan.create()
        self.screen = pygame.display.set_mode((0, 0), flags=pygame.RESIZABLE)
        self.running = True
        self.FPS = 30
        self._init()

    def _init(self):
        # images
        self.image_manager.add(ImageNames.MOUSE, 'resources/mouse.png')
        self.image_manager.add(ImageNames.BOX, ((44, 44, 55), (50, 50)))

        # sprites
        self.sprite_manager.add(SpriteNames.MOUSE1, ImageNames.MOUSE, 35, 35, 200, 200)
        self.sprite_manager.add(SpriteNames.MOUSE1, ImageNames.MOUSE, 50, 50, 300, 300)
        self.sprite_manager.add(SpriteNames.MOUSE2, ImageNames.MOUSE, 50, 50, 400, 400)
        self.sprite_manager.add(SpriteNames.MOUSE2, ImageNames.MOUSE, 50, 50, 500, 500)
        self.sprite_manager.add(SpriteNames.BOX, ImageNames.BOX, 50, 50, 100, 100)

        mouse_sprite = GameSprite(SpriteNames.MOUSE2, ImageNames.MOUSE, (52, 27), (200, 200))
        self.gamesprite_manager.add([mouse_sprite])

        # input
        lmouse_subject = LMouseClickCircle()
        rmouse_subject = RMouseClickCircle()
        self.input_manager.lmouse.attach(lmouse_subject)
        self.input_manager.rmouse.attach(rmouse_subject)

        # timer
        self.timer_manager = TimerMan.create()

    def draw(self):

        # render sprites and stuff
        self.gamesprite_manager.draw(self.screen)
        self.sprite_manager.draw(self.screen)
        self.boxsprite_manager.draw(self.screen)

        # update the display
        pygame.display.update()

        # clear the display
        self.screen.fill((0, 0, 0))

    def update(self):
        # input updates
        self.input_manager.update(self)

        # update the sprites
        self.gamesprite_manager.update()
        self.sprite_manager.update()
        self.boxsprite_manager.update()

        # update the timer events
        self.timer_manager.update(self, pygame.time.get_ticks())

    def run(self):
        pygame.init()

        # Fill the background with black
        self.screen.fill((0, 0, 0))

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

