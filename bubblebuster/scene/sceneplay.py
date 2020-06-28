from bubblebuster.input import LMouseClickCircleObserver, RMouseClickCircleObserver
from bubblebuster.sound import Music, SoundNames
from bubblebuster.settings import GameSettings, InterfaceSettings, SCREEN_HEIGHT, SCREEN_WIDTH
from bubblebuster.player import PlayerNames, Player
from bubblebuster.font import FontNames, Font
from bubblebuster.collision import CollisionRectPair
from bubblebuster.scene import Scene
from bubblebuster.sprite import CircleFactory


import pygame


class ScenePlay(Scene):
    def __init__(self, name, game, player=None):
        super().__init__(name, game)
        # images
        #self.image_manager.add(ImageNames.EXPLODE, 'resources/explode.png')

        # zounds
        self.sound_manager.add(SoundNames.SMALLEXPLODE, 'resources/small_explode.wav')
        self.sound_manager.add(SoundNames.LARGEEXPLODE, 'resources/large_explode.wav')
        self.sound_manager.add(SoundNames.BUBBLE_MINIPOP, 'resources/bubble_mini_pop.wav')
        self.sound_manager.add(SoundNames.BUBBLE_SMALLPOP, 'resources/bubble_small_pop.wav')
        self.sound_manager.add(SoundNames.BUBBLE_MEDIUMPOP, 'resources/bubble_medium_pop.wav')
        self.sound_manager.add(SoundNames.BUBBLE_LARGEPOP, 'resources/bubble_large_pop.wav')

        # input
        self.input_manager.lmouse.attach(LMouseClickCircleObserver())
        self.input_manager.rmouse.attach(RMouseClickCircleObserver())

        if not player:
            # player
            player = Player(PlayerNames.PLAYERONE, 
                            GameSettings.PLAYER_EXPLOSIONS, 
                            GameSettings.NUMBER_OF_BUBBLES
            )
        self.playerone = self.player_manager.add(player)


    def update(self):
        time = pygame.time.get_ticks()

        # input updates
        self.input_manager.update(self.game)

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

        # player
        self.player_manager.update()

    def draw(self):
        # render sprites and stuff
        self.sprite_manager.draw(self.screen)
        self.boxsprite_manager.draw(self.screen)

        # fonts
        self.font_manager.draw(self.screen)

    def handle(self, player=None):
        musicmenu = Music(SoundNames.MUSICMENU, 'resources/bubbles.wav')
        musicmenu.play()


        # sprites
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(GameSettings.NUMBER_OF_BUBBLES, 
                                       max_xy=(SCREEN_WIDTH, 
                                               SCREEN_HEIGHT), 
                                       max_h=GameSettings.BUBBLE_MAXH
        )

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)

        # fonts
        MENU_STARTX = 10
        MENU_STARTY = 15
        MENU_OFFSETY = 20
        MENU_OFFSETX = 150

        self.font_manager.add(Font(FontNames.LEVEL, InterfaceSettings.FONTSTYLE, 16, 'Level: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.SCORE, InterfaceSettings.FONTSTYLE, 16, self.playerone.current_level, InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_STARTY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Round: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.SCOREROUND, InterfaceSettings.FONTSTYLE, 16, self.playerone.score, InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Score: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.SCORE, InterfaceSettings.FONTSTYLE, 16, self.playerone.score, InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Bubbles: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.BUBBLES, InterfaceSettings.FONTSTYLE, 16, self.playerone.bubbles, InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Explosions: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.EXPLOSIONS, InterfaceSettings.FONTSTYLE, 16, self.playerone.explosions, InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Time: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_timedisplay = self.font_manager.add(Font(FontNames.TIME, InterfaceSettings.FONTSTYLE, 16, self.timer_manager.current_time, InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))

        self.font_manager.add(Font(FontNames.TOAST, InterfaceSettings.FONTSTYLE, 16, '', InterfaceSettings.FONTCOLOR, (SCREEN_WIDTH-150, SCREEN_HEIGHT-25)))

        font = self.font_manager.find(FontNames.SCOREROUND)
        font.text = 0