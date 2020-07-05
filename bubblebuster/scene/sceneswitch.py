from bubblebuster.sprite import CircleFactory
from bubblebuster.sound import SoundNames
from bubblebuster.settings import InterfaceSettings
from bubblebuster.collision import CollisionRectPair
from bubblebuster.font import Font, FontNames
from bubblebuster.timer import SwitchSceneCommand
from bubblebuster.settings import InterfaceSettings
import bubblebuster.player as pl
import bubblebuster.scene.scene as sc
import bubblebuster.scene.scenecontext as sccxt
import bubblebuster.scene.sceneplay as scpl
import bubblebuster.level as le

from math import inf
import pygame


class SceneSwitch(sc.Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

        # zounds
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')
        self.sound_manager.add_music(SoundNames.MUSICMENU, 'resources/bubbling.wav')

        # make some bubbles
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(10,
                                       max_xy=(InterfaceSettings.SCREEN_WIDTH,
                                               InterfaceSettings.SCREEN_HEIGHT),
                                       max_h=250
        )

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)

        MENU_STARTX = InterfaceSettings.SCREEN_WIDTH // 8
        MENU_STARTY = InterfaceSettings.SCREEN_HEIGHT // 3
        MENU_OFFSETY = 45
        MENU_OFFSETX = InterfaceSettings.SCREEN_WIDTH // 3
        MENU_OFFSETX_ARROW = 50

        self.font_manager.add(Font(FontNames.MENUTITLE,
                                        InterfaceSettings.FONTSTYLE,
                                        48,
                                        'Level %d' % 1,
                                        InterfaceSettings.FONTCOLOR,
                                        (InterfaceSettings.SCREEN_WIDTH // 8, InterfaceSettings.SCREEN_HEIGHT // 8)
                                        )
                                   )

        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 20, 'Round Score', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        self.font_manager.add(Font(FontNames.STATS_EXPLOSIONBONUSA, InterfaceSettings.FONTSTYLE, 20, '0', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_EXPLOSIONBONUSB, InterfaceSettings.FONTSTYLE, 20, '', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_EXPLOSIONBONUSC, InterfaceSettings.FONTSTYLE, 20, '', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_EXPLOSIONBONUSD, InterfaceSettings.FONTSTYLE, 20, '', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW*2, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_ROUNDSCORE, InterfaceSettings.FONTSTYLE, 20, '', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW*3, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_ROUNDSCORE, InterfaceSettings.FONTSTYLE, 20, '', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 20, 'Total Score', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_SCORE, InterfaceSettings.FONTSTYLE, 20, 0, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 20, '# of Bubbles', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_BUBBLES, InterfaceSettings.FONTSTYLE, 20, 0, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 20, 'Max Multiplier', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_MAXMULTIPLIER, InterfaceSettings.FONTSTYLE, 20, 0, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 20, 'Explosions in Round', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_EXPLOSIONSUSEDPREV, InterfaceSettings.FONTSTYLE, 20, 0, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 20, 'Total Explosions', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_EXPLOSIONSUSED, InterfaceSettings.FONTSTYLE, 20, 0, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY*2
        self.font_manager.add(Font(FontNames.SCENESWITCH_PRESSANYKEY, InterfaceSettings.FONTSTYLE, 20, 'Press any key ...', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

    def update(self):
        time = pygame.time.get_ticks()

        # input updates
        self.input_manager.update(self.game)

        # sprites
        self.boxsprite_manager.update()

        # collisions
        self.collisionpair_manager.process()

        # fonts ...
        self.font_manager.update()

        # time
        self.timer_manager.update(self, time)

    def draw(self):
        self.boxsprite_manager.draw(self.screen)

        self.font_manager.draw(self.screen)

    def handle(self):
        musicmenu = self.sound_manager.find(SoundNames.MUSICMENU)
        musicmenu.play()

        player = pl.PlayerMan.instance.find(pl.PlayerNames.PLAYERONE)

        if player:
            menutitle = self.font_manager.find(FontNames.MENUTITLE)
            menutitle.text = 'Level %d' % le.LevelMan.instance.current_level.level

            MENU_STARTX = InterfaceSettings.SCREEN_WIDTH // 8
            MENU_STARTY = InterfaceSettings.SCREEN_HEIGHT // 3
            MENU_OFFSETX = InterfaceSettings.SCREEN_WIDTH // 3
            MENU_OFFSETX_ARROW = 50

            fontstatsexplosionbonusA = self.font_manager.find(FontNames.STATS_EXPLOSIONBONUSA)
            fontstatsexplosionbonusB = self.font_manager.find(FontNames.STATS_EXPLOSIONBONUSB)
            fontstatsexplosionbonusC = self.font_manager.find(FontNames.STATS_EXPLOSIONBONUSC)
            fontstatsexplosionbonusD = self.font_manager.find(FontNames.STATS_EXPLOSIONBONUSD)
            fontstatsscoreval = self.font_manager.find(FontNames.STATS_ROUNDSCORE)

            if player.weapon.ammo < inf and player.stats_explosionsprev: # do the thing
                fontstatsexplosionbonusA.text = player.stats_scoreroundprev//player.stats_explosionsprev
                fontstatsexplosionbonusA.posxy = (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)
                w, h = fontstatsexplosionbonusA.font.size(str(fontstatsexplosionbonusA.text))
                w += MENU_OFFSETX_ARROW
                fontstatsexplosionbonusB.text = 'x'
                fontstatsexplosionbonusB.posxy = (MENU_STARTX+MENU_OFFSETX+w, MENU_STARTY)
                fontstatsexplosionbonusC.text = player.stats_explosionsprev
                fontstatsexplosionbonusC.posxy = (MENU_STARTX+MENU_OFFSETX+w+MENU_OFFSETX_ARROW, MENU_STARTY)
                fontstatsexplosionbonusD.text = '='
                fontstatsexplosionbonusD.posxy = (MENU_STARTX+MENU_OFFSETX+w+MENU_OFFSETX_ARROW*2, MENU_STARTY)
                fontstatsscoreval.text = player.stats_scoreroundprev
                fontstatsscoreval.posxy = (MENU_STARTX+MENU_OFFSETX+w+MENU_OFFSETX_ARROW*3, MENU_STARTY)
            else:
                fontstatsexplosionbonusA.text = ''
                fontstatsexplosionbonusB.text = ''
                fontstatsexplosionbonusC.text = ''
                fontstatsexplosionbonusD.text = ''
                fontstatsscoreval.text = player.stats_scoreroundprev
                fontstatsscoreval.posxy = (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)

            fontstatstotalscoreval = self.font_manager.find(FontNames.STATS_SCORE)
            fontstatstotalscoreval.text = player.score
            fontstatsbubblesval = self.font_manager.find(FontNames.STATS_BUBBLES)
            fontstatsbubblesval.text = player.stats_bubbles
            fontstatsmultval = self.font_manager.find(FontNames.STATS_MAXMULTIPLIER)
            fontstatsmultval.text = player.stats_maxmultiplier
            fontstatsexplosionsusedprevval = self.font_manager.find(FontNames.STATS_EXPLOSIONSUSEDPREV)
            fontstatsexplosionsusedprevval.text = player.weapon.stats_usedroundprev
            fontstatsexplosionsusedval = self.font_manager.find(FontNames.STATS_EXPLOSIONSUSED)
            fontstatsexplosionsusedval.text = player.stats_explosions

        # hack me
        #sccxt.SceneContext.instance.scene_play = scpl.ScenePlay(sc.SceneNames.PLAY, self.game)
        self.timer_manager.add(SwitchSceneCommand(sc.SceneNames.PLAY, onkeypress=True), 0)

