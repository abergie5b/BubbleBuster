from bubblebuster.input import LMouseClickCircleObserver, RMouseClickCircleObserver
from bubblebuster.sound import Music, SoundNames
from bubblebuster.settings import GameSettings, InterfaceSettings
from bubblebuster.player import PlayerNames, Player
from bubblebuster.font import FontNames, Font
from bubblebuster.collision import CollisionRectPair
from bubblebuster.scene import Scene
from bubblebuster.sprite import CircleFactory, LineSpriteNames


import pygame


class ScenePlay(Scene):
    def __init__(self, name, game, player=None):
        super().__init__(name, game)

        SCREEN_WIDTH, SCREEN_HEIGHT = (InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT)

        self.player = self.player_manager.add(player)
        wallbottom = self.boxsprite_manager.find(LineSpriteNames.WALL_BOTTOM)
        startxy = (wallbottom.start_xy[0], wallbottom.start_xy[1]-35)
        endxy = (wallbottom.end_xy[0], wallbottom.end_xy[1]-35)
        wallbottom.set_coords(startxy, endxy)

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

        # fonts
        MENU_STARTX = 10
        MENU_STARTY = 15
        MENU_OFFSETY = 20
        MENU_OFFSETX = 150

        self.font_manager.add(Font(FontNames.LEVEL, InterfaceSettings.FONTSTYLE, 16, 'Level: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.CURRENTLEVEL, InterfaceSettings.FONTSTYLE, 16, '', InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_STARTY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Round: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.SCOREROUND, InterfaceSettings.FONTSTYLE, 16, '', InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Score: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.SCORE, InterfaceSettings.FONTSTYLE, 16, '', InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Bubbles: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.BUBBLES, InterfaceSettings.FONTSTYLE, 16, '', InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Explosions: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_manager.add(Font(FontNames.EXPLOSIONS, InterfaceSettings.FONTSTYLE, 16, '', InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))
        MENU_OFFSETY += MENU_STARTY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, 'Time: ', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_OFFSETY)))
        self.font_timedisplay = self.font_manager.add(Font(FontNames.TIME, InterfaceSettings.FONTSTYLE, 16, '', InterfaceSettings.FONTCOLOR, (MENU_OFFSETX, MENU_OFFSETY)))

        self.font_manager.add(Font(FontNames.TOAST, InterfaceSettings.FONTSTYLE, 16, '', InterfaceSettings.FONTCOLOR, (SCREEN_WIDTH-SCREEN_WIDTH//10, SCREEN_HEIGHT-25)))

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
        assert(player)

        self.player = self.player

        musicmenu = Music(SoundNames.MUSICMENU, 'resources/bubbles.wav')
        musicmenu.play()

        # sprites
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(GameSettings.NUMBER_OF_BUBBLES, 
                                       max_xy=(InterfaceSettings.SCREEN_WIDTH,
                                               InterfaceSettings.SCREEN_HEIGHT-35),
                                       max_h=GameSettings.BUBBLE_MAXH
        )

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)

        # fonts
        fontcurrentlevel = self.font_manager.find(FontNames.CURRENTLEVEL)
        fontcurrentlevel.text = self.player.current_level
        fontscoreround = self.font_manager.find(FontNames.SCOREROUND)
        fontscoreround.text = 0
        fontscore = self.font_manager.find(FontNames.SCORE)
        fontscore.text = self.player.score
        fontbubbles = self.font_manager.find(FontNames.BUBBLES)
        fontbubbles.text = self.player.bubbles
        fontexplosions = self.font_manager.find(FontNames.EXPLOSIONS)
        fontexplosions.text = self.player.weapon.ammo
        fonttime = self.font_manager.find(FontNames.TIME)
        fonttime.text = self.timer_manager.current_time

