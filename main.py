import pygame

from input import InputMan, LMouseClickCircle, RMouseClickCircle
from image import ImageMan, ImageNames
from sprite import BoxSpriteMan, BoxSpriteNames, LineSprite, LineSpriteNames, SpriteMan
from collision import CollisionCirclePair, CollisionRectPair, CollisionPairMan
from timer import TimerMan

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Game:
    def __init__(self):
        self.image_manager = ImageMan.create()
        self.sprite_manager = SpriteMan.create()
        self.boxsprite_manager = BoxSpriteMan.create(self)
        self.input_manager = InputMan.create()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
        self.running = True
        self.FPS = 90
        self._init()

    def _init(self):
        # images
        self.image_manager.add(ImageNames.EXPLODE, 'resources/explode.png')

        # sprites
        self.circleA = self.boxsprite_manager.add(BoxSpriteNames.CIRCLEA, 0, 50, 100, 100, color=(255, 0, 0))
        self.circleB = self.boxsprite_manager.add(BoxSpriteNames.CIRCLEB, 0, 50, 200, 200, color=(0, 255, 0))
        self.circleC = self.boxsprite_manager.add(BoxSpriteNames.CIRCLEC, 0, 50, 300, 300, color=(0, 0, 255))
        self.circleD = self.boxsprite_manager.add(BoxSpriteNames.CIRCLED, 0, 50, 400, 400, color=(125, 125, 125))
        self.circleE = self.boxsprite_manager.add(BoxSpriteNames.CIRCLEE, 0, 50, 500, 500, color=(255, 255, 0))

        # walls
        self.wall_left = self.boxsprite_manager.add_line_sprite(LineSpriteNames.WALL_LEFT, (0, 0), (0, SCREEN_HEIGHT), color=(255, 0, 0), width=2)
        self.wall_right = self.boxsprite_manager.add_line_sprite(LineSpriteNames.WALL_RIGHT, (SCREEN_WIDTH-2, 0), (SCREEN_WIDTH-2, SCREEN_HEIGHT), color=(0, 255, 0), width=2)
        self.wall_top = self.boxsprite_manager.add_line_sprite(LineSpriteNames.WALL_TOP, (0, 0), (SCREEN_WIDTH, 0), color=(0, 255, 255), width=2)
        self.wall_bottom = self.boxsprite_manager.add_line_sprite(LineSpriteNames.WALL_BOTTOM, (0, SCREEN_HEIGHT-2), (SCREEN_WIDTH, SCREEN_HEIGHT-2), color=(255, 255, 0), width=2)

        # input
        lmouse_subject = LMouseClickCircle()
        rmouse_subject = RMouseClickCircle()
        self.input_manager.lmouse.attach(lmouse_subject)
        self.input_manager.rmouse.attach(rmouse_subject)

        # timer
        self.timer_manager = TimerMan.create()

        # collisions
        self.collisionpair_manager = CollisionPairMan.create()

        self.collisionpair_manager.add(CollisionCirclePair(self.circleA, self.circleB))
        self.collisionpair_manager.add(CollisionCirclePair(self.circleA, self.circleC))
        self.collisionpair_manager.add(CollisionCirclePair(self.circleA, self.circleD))
        self.collisionpair_manager.add(CollisionCirclePair(self.circleA, self.circleE))

        self.collisionpair_manager.add(CollisionCirclePair(self.circleB, self.circleC))
        self.collisionpair_manager.add(CollisionCirclePair(self.circleB, self.circleD))
        self.collisionpair_manager.add(CollisionCirclePair(self.circleB, self.circleE))

        self.collisionpair_manager.add(CollisionCirclePair(self.circleC, self.circleD))
        self.collisionpair_manager.add(CollisionCirclePair(self.circleC, self.circleE))

        self.collisionpair_manager.add(CollisionCirclePair(self.circleD, self.circleE))

        self.collisionpair_manager.add(CollisionRectPair(self.wall_left, self.circleA))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_right, self.circleA))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_top, self.circleA))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_bottom, self.circleA))

        self.collisionpair_manager.add(CollisionRectPair(self.wall_left, self.circleB))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_right, self.circleB))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_top, self.circleB))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_bottom, self.circleB))

        self.collisionpair_manager.add(CollisionRectPair(self.wall_left, self.circleC))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_right, self.circleC))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_top, self.circleC))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_bottom, self.circleC))

        self.collisionpair_manager.add(CollisionRectPair(self.wall_left, self.circleD))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_right, self.circleD))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_top, self.circleD))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_bottom, self.circleD))

        self.collisionpair_manager.add(CollisionRectPair(self.wall_left, self.circleE))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_right, self.circleE))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_top, self.circleE))
        self.collisionpair_manager.add(CollisionRectPair(self.wall_bottom, self.circleE))

    def draw(self):
        # render sprites and stuff
        self.sprite_manager.draw(self.screen)
        self.boxsprite_manager.draw(self.screen)

        # draw the entire screen
        pygame.display.update()

        # clear the display
        # is there ... a better way? -.-
        self.screen.fill((0, 0, 0))

    def update(self):
        # input updates
        self.input_manager.update(self)

        # update the sprites
        self.sprite_manager.update()
        self.boxsprite_manager.update()

        # update the timer events
        self.timer_manager.update(self, pygame.time.get_ticks())

        # update collision events
        self.collisionpair_manager.process()

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

