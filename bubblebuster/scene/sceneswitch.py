from bubblebuster.sprite import CircleFactory
from bubblebuster.sound import SoundNames, Music
from bubblebuster.scene import Scene, SceneContext, SceneNames, ScenePlay
from bubblebuster.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from bubblebuster.collision import CollisionRectPair
from bubblebuster.font import Font, FontNames
from bubblebuster.timer import SwitchSceneCommand
from bubblebuster.settings import InterfaceSettings, GameSettings


import pygame


class SceneSwitch(Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

        # zounds
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')
        
        # make some bubbles
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(10,
                                       max_xy=(SCREEN_WIDTH, 
                                               SCREEN_HEIGHT), 
                                       max_h=100
        )

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)

        MENU_STARTX = SCREEN_WIDTH // 4
        MENU_STARTY = SCREEN_HEIGHT // 3
        MENU_OFFSETY = 45
        MENU_OFFSETX = 350
        MENU_OFFSETX_ARROW = 50

        self.font_manager.add(Font(FontNames.MENUTITLE,
                                        InterfaceSettings.FONTSTYLE,
                                        48,
                                        'Level %d' % 1,
                                        InterfaceSettings.FONTCOLOR,
                                        (SCREEN_WIDTH // 7, SCREEN_HEIGHT // 6)
                                        )
                                   )

        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Round Score', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        self.font_manager.add(Font(FontNames.STATS_EXPLOSIONBONUSA, InterfaceSettings.FONTSTYLE, 24, '0', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_EXPLOSIONBONUSB, InterfaceSettings.FONTSTYLE, 24, '', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_EXPLOSIONBONUSC, InterfaceSettings.FONTSTYLE, 24, '', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_EXPLOSIONBONUSD, InterfaceSettings.FONTSTYLE, 24, '', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW*2, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_ROUNDSCORE, InterfaceSettings.FONTSTYLE, 24, '', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW*3, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_ROUNDSCORE, InterfaceSettings.FONTSTYLE, 24, '', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Total Score', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_SCORE, InterfaceSettings.FONTSTYLE, 24, 0, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '# of Bubbles', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_BUBBLES, InterfaceSettings.FONTSTYLE, 24, 0, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Max Multiplier', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_MAXMULTIPLIER, InterfaceSettings.FONTSTYLE, 24, 0, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Explosions in Round', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_EXPLOSIONSUSEDPREV, InterfaceSettings.FONTSTYLE, 24, 0, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Total Explosions', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.STATS_EXPLOSIONSUSED, InterfaceSettings.FONTSTYLE, 24, 0, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY*2
        self.font_manager.add(Font(FontNames.SCENESWITCH_PRESSANYKEY, InterfaceSettings.FONTSTYLE, 24, 'Press any key ...', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

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

    def handle(self, player=None):
        musicmenu = Music(SoundNames.MUSICMENU, 'resources/bubbling.wav')
        musicmenu.play()

        if player:
            menutitle = self.font_manager.find(FontNames.MENUTITLE)
            menutitle.text = 'Level %d' % player.current_level

            MENU_STARTX = SCREEN_WIDTH // 4
            MENU_STARTY = SCREEN_HEIGHT // 3
            MENU_OFFSETX = 350
            MENU_OFFSETX_ARROW = 50

            fontstatsexplosionbonusA = self.font_manager.find(FontNames.STATS_EXPLOSIONBONUSA)
            fontstatsexplosionbonusB = self.font_manager.find(FontNames.STATS_EXPLOSIONBONUSB)
            fontstatsexplosionbonusC = self.font_manager.find(FontNames.STATS_EXPLOSIONBONUSC)
            fontstatsexplosionbonusD = self.font_manager.find(FontNames.STATS_EXPLOSIONBONUSD)
            fontstatsscoreval = self.font_manager.find(FontNames.STATS_ROUNDSCORE)

            if player.stats_explosionsprev: # do the thing
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
                fontstatsexplosionbonusA = ''
                fontstatsexplosionbonusB = ''
                fontstatsexplosionbonusC = ''
                fontstatsexplosionbonusD = ''
                fontstatsscoreval.text = player.stats_scoreroundprev
                fontstatsscoreval.posxy = (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)

            fontstatstotalscoreval = self.font_manager.find(FontNames.STATS_SCORE)
            fontstatstotalscoreval.text = player.score
            fontstatsbubblesval = self.font_manager.find(FontNames.STATS_BUBBLES)
            fontstatsbubblesval.text = player.stats_bubbles
            fontstatsmultval = self.font_manager.find(FontNames.STATS_MAXMULTIPLIER)
            fontstatsmultval.text = player.stats_maxmultiplier
            fontstatsexplosionsusedprevval = self.font_manager.find(FontNames.STATS_EXPLOSIONSUSEDPREV)
            fontstatsexplosionsusedprevval.text = GameSettings.PLAYER_EXPLOSIONS-player.stats_explosionsprev
            fontstatsexplosionsusedval = self.font_manager.find(FontNames.STATS_EXPLOSIONSUSED)
            fontstatsexplosionsusedval.text = player.stats_explosions

        #  i dont want to have to do this
        # its needed and i dont know why mate
        SceneContext.instance.reset(player=player)

        self.timer_manager.add(SwitchSceneCommand(SceneNames.PLAY, onkeypress=True), 0)
