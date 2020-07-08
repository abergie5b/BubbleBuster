from bubblebuster.input import LMouseClickShootObserver, RMouseClickShootObserver, Simulation
from bubblebuster.sound import SoundNames
from bubblebuster.settings import GameSettings, InterfaceSettings
from bubblebuster.font import FontNames, Font
from bubblebuster.collision import CollisionRectPair
from bubblebuster.sprite import CircleFactory, LineSpriteNames
import bubblebuster.scene.scene as sc
import bubblebuster.player as pl
import bubblebuster.level as le
import bubblebuster.timer as ti
import bubblebuster.scene.sceneswitch as scsw


import pygame


class ScenePlay(sc.Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

        SCREEN_WIDTH, SCREEN_HEIGHT = (InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT)

        # zounds
        self.sound_manager.add(SoundNames.SMALLEXPLODE, 'resources/small_explode.wav')
        self.sound_manager.add(SoundNames.LARGEEXPLODE, 'resources/large_explode.wav')
        self.sound_manager.add(SoundNames.BUBBLE_MINIPOP, 'resources/bubble_mini_pop.wav')
        self.sound_manager.add(SoundNames.BUBBLE_SMALLPOP, 'resources/bubble_small_pop.wav')
        self.sound_manager.add(SoundNames.BUBBLE_MEDIUMPOP, 'resources/bubble_medium_pop.wav')
        self.sound_manager.add(SoundNames.BUBBLE_LARGEPOP, 'resources/bubble_large_pop.wav')
        self.sound_manager.add_music(SoundNames.MUSICMENU, 'resources/bubbles.wav')

        # input
        self.input_manager.lmouse.attach(LMouseClickShootObserver())
        self.input_manager.rmouse.attach(RMouseClickShootObserver())

        # player
        self.player = pl.PlayerMan.instance.find(pl.PlayerNames.PLAYERONE)
        assert self.player

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

        self.font_manager.add(Font(FontNames.TOAST, InterfaceSettings.FONTSTYLE, 16, '', InterfaceSettings.FONTCOLOR, (SCREEN_WIDTH//24, SCREEN_HEIGHT-25)))

        # maybe we'll use this
        self.target_time = 0

    def update(self):
        time = pygame.time.get_ticks()

        Simulation.instance.update(time)

        # input updates
        self.input_manager.update(self.game)

        if Simulation.instance.time_step > 0:

            # update the sprites
            self.sprite_manager.update()
            self.boxsprite_manager.update()

            # update the timer events
            self.timer_manager.update(self, time)

            # fonts
            # poo poo
            if self.target_time:
                time = self.target_time - ti.TimerMan.instance.current_time
                self.font_timedisplay.text = '%s.%s' % (time // 1000, str(time)[-3:-1])
            self.font_manager.update()

            # update collision events
            self.collisionpair_manager.process()

            # level
            le.LevelMan.instance.update()

            # player
            pl.PlayerMan.instance.update()

    def draw(self):
        # render sprites and stuff
        self.sprite_manager.draw(self.screen)
        self.boxsprite_manager.draw(self.screen)

        # fonts
        self.font_manager.draw(self.screen)

    def handle(self):
        musicmenu = self.sound_manager.find(SoundNames.MUSICMENU)
        musicmenu.play()

        # sprites
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(le.LevelMan.instance.current_level.bubbles,
                                       max_xy=(InterfaceSettings.SCREEN_WIDTH,
                                               InterfaceSettings.SCREEN_HEIGHT),
                                       max_h=le.LevelMan.instance.current_level.bubble_maxh
                                       )

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)

        # fonts
        fontcurrentlevel = self.font_manager.find(FontNames.CURRENTLEVEL)
        fontcurrentlevel.text = le.LevelMan.instance.current_level.level
        fontscoreround = self.font_manager.find(FontNames.SCOREROUND)
        fontscoreround.text = 0
        fontscore = self.font_manager.find(FontNames.SCORE)
        fontscore.text = self.player.score
        fontbubbles = self.font_manager.find(FontNames.BUBBLES)
        fontbubbles.text = le.LevelMan.instance.current_level.bubbles
        fontexplosions = self.font_manager.find(FontNames.EXPLOSIONS)
        fontexplosions.text = self.player.weapon.stats_usedround
        fonttime = self.font_manager.find(FontNames.TIME)

        time = le.LevelMan.instance.current_level.target_time
        current_time = self.timer_manager.current_time
        if time:
            self.target_time = time + current_time
            self.timer_manager.add(ti.SetGameOverCommand(), time)
        else:
            self.target_time = 0
        fonttime.text = '%s.%s' % (time // 1000, str(time)[-3:-1])

