import pygame

from input import InputMan, LMouseClickCircle, RMouseClickCircle
from image import ImageMan, ImageNames
from sprite import BoxSpriteMan, BoxSpriteNames, LineSprite, LineSpriteNames, SpriteMan
from collision import CollisionCirclePair, CollisionRectPair, CollisionPairMan
from timer import TimerMan
from groups import CircleGroup, Group, GroupMan, GroupNames
from factory import CircleFactory
from font import Font, FontMan, FontNames
from player import Player, PlayerMan, PlayerNames

from settings import *


class Game:
    def __init__(self):
        self.image_manager = ImageMan.create()
        self.sprite_manager = SpriteMan.create()
        self.boxsprite_manager = BoxSpriteMan.create()
        self.input_manager = InputMan.create()
        self.group_manager = GroupMan.create()
        self.collisionpair_manager = CollisionPairMan.create()
        self.font_manager = FontMan.create()
        self.player_manager = PlayerMan.create()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
        self.running = True
        self.FPS = 90
        self._init()

    def _init(self):
        pygame.init()

        # images
        self.image_manager.add(ImageNames.EXPLODE, 'resources/explode.png')

        # groups
        self.circle_group = CircleGroup(GroupNames.CIRCLE)
        self.wall_group = Group(GroupNames.WALL)

        self.group_manager.add(self.wall_group)
        self.group_manager.add(self.circle_group)

        # walls
        self.wall_left = self.boxsprite_manager.add_line_sprite(LineSpriteNames.WALL_LEFT, (0, 0), (0, SCREEN_HEIGHT), color=(255, 0, 0), width=2)
        self.wall_right = self.boxsprite_manager.add_line_sprite(LineSpriteNames.WALL_RIGHT, (SCREEN_WIDTH-2, 0), (SCREEN_WIDTH-2, SCREEN_HEIGHT), color=(0, 255, 0), width=2)
        self.wall_top = self.boxsprite_manager.add_line_sprite(LineSpriteNames.WALL_TOP, (0, 0), (SCREEN_WIDTH, 0), color=(0, 255, 255), width=2)
        self.wall_bottom = self.boxsprite_manager.add_line_sprite(LineSpriteNames.WALL_BOTTOM, (0, SCREEN_HEIGHT-2), (SCREEN_WIDTH, SCREEN_HEIGHT-2), color=(255, 255, 0), width=2)
        
        self.wall_group.add(self.wall_left)
        self.wall_group.add(self.wall_right)
        self.wall_group.add(self.wall_top)
        self.wall_group.add(self.wall_bottom)

        # input
        lmouse_subject = LMouseClickCircle()
        rmouse_subject = RMouseClickCircle()

        self.input_manager.lmouse.attach(lmouse_subject)
        self.input_manager.rmouse.attach(rmouse_subject)

        # timer
        self.timer_manager = TimerMan.create()

        # sprites
        circle_factory = CircleFactory(self.circle_group)
        circle_factory.generate_random(GameSettings.NUMBER_OF_BUBBLES, 
                                       max_xy=(SCREEN_WIDTH-GameSettings.BUBBLE_MAXH, 
                                               SCREEN_HEIGHT-GameSettings.BUBBLE_MAXH), 
                                       max_h=GameSettings.BUBBLE_MAXH
        )

        # player
        player = Player(PlayerNames.PLAYERONE, GameSettings.PLAYER_EXPLOSIONS, GameSettings.PLAYER_LIVES, GameSettings.NUMBER_OF_BUBBLES)
        self.playerone = self.player_manager.add(player)

        # fonts
        MENU_STARTX = 10
        MENU_STARTY = 15
        MENU_OFFSETY = 15
        MENU_OFFSETX = 80
        #FontMan.instance.add(Font(FontNames.TITLE, 'Comic Sans', 16, 'Bubble Busters', (255, 255, 255), (10, 10)))
        FontMan.instance.add(Font(FontNames.NULL, 'Comic Sans', 16, 'Explosions: ', (255, 255, 255), (MENU_STARTX, MENU_STARTY)))
        FontMan.instance.add(Font(FontNames.EXPLOSIONS, 'Comic Sans', 16, self.playerone.explosions, (255, 255, 255), (MENU_OFFSETX, MENU_STARTY)))
        MENU_OFFSETY += MENU_STARTY
        FontMan.instance.add(Font(FontNames.NULL, 'Comic Sans', 16, 'Lives: ', (255, 255, 255), (MENU_STARTX, MENU_OFFSETY)))
        FontMan.instance.add(Font(FontNames.LIVES, 'Comic Sans', 16, self.playerone.lives, (255, 255, 255), (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        FontMan.instance.add(Font(FontNames.NULL, 'Comic Sans', 16, 'Score: ', (255, 255, 255), (MENU_STARTX, MENU_OFFSETY)))
        FontMan.instance.add(Font(FontNames.SCORE, 'Comic Sans', 16, self.playerone.score, (255, 255, 255), (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        FontMan.instance.add(Font(FontNames.NULL, 'Comic Sans', 16, 'Multiplier: ', (255, 255, 255), (MENU_STARTX, MENU_OFFSETY)))
        FontMan.instance.add(Font(FontNames.MULTIPLIER_TITLE, 'Comic Sans', 16, 0, (255, 255, 255), (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        FontMan.instance.add(Font(FontNames.NULL, 'Comic Sans', 16, 'Bubbles: ', (255, 255, 255), (MENU_STARTX, MENU_OFFSETY)))
        FontMan.instance.add(Font(FontNames.BUBBLES, 'Comic Sans', 16, GameSettings.NUMBER_OF_BUBBLES, (255, 255, 255), (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        FontMan.instance.add(Font(FontNames.NULL, 'Comic Sans', 16, 'Time: ', (255, 255, 255), (MENU_STARTX, MENU_OFFSETY)))
        self.font_timedisplay = FontMan.instance.add(Font(FontNames.TIME, 'Comic Sans', 16, self.timer_manager.instance.current_time, (255, 255, 255), (MENU_OFFSETX, MENU_OFFSETY)))

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)

    def draw(self):
        # render sprites and stuff
        self.sprite_manager.draw(self.screen)
        self.boxsprite_manager.draw(self.screen)

        # fonts
        self.font_manager.draw(self.screen)

        # draw the entire screen
        pygame.display.update()

        # clear the display
        # is there ... a better way? -.-
        self.screen.fill((0, 0, 0))

    def update(self):
        time = pygame.time.get_ticks()

        # input updates
        self.input_manager.update(self)

        # update the sprites
        self.sprite_manager.update()
        self.boxsprite_manager.update()

        # update the timer events
        self.timer_manager.update(self, time)

        # fonts
        # poo poo
        self.font_timedisplay.text = '%s.%s' % (time // 1000, str(time)[-3:-1])
        self.font_manager.update()

        # update collision events
        self.collisionpair_manager.process()

    def run(self):

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

