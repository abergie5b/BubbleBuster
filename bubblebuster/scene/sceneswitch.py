from bubblebuster.sprite import CircleFactory
from bubblebuster.sound import SoundNames, Music
from bubblebuster.scene import Scene, SceneContext, SceneNames
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

        menutitle = self.font_manager.add(Font(FontNames.MENUTITLE, 
                                   InterfaceSettings.FONTSTYLE,
                                   48, 
                                   'Level %d' % player.current_level,
                                   InterfaceSettings.FONTCOLOR, 
                                   (SCREEN_WIDTH//7, SCREEN_HEIGHT//6)
                              )
        )

        MENU_STARTX = SCREEN_WIDTH // 4
        MENU_STARTY = SCREEN_HEIGHT // 3
        MENU_OFFSETY = 45
        MENU_OFFSETX = 350
        MENU_OFFSETX_ARROW = 50

        fontstatsscore = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Round Score', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        if player.stats_explosionsprev:
            fontstatsexplosionbonusA = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, player.stats_scoreroundprev//player.stats_explosionsprev, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
            w, h = fontstatsexplosionbonusA.font.size(str(fontstatsexplosionbonusA.text))
            w += MENU_OFFSETX_ARROW
            fontstatsexplosionbonusB = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'x', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+w, MENU_STARTY)))
            fontstatsexplosionbonusC = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, player.stats_explosionsprev, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+w+MENU_OFFSETX_ARROW, MENU_STARTY)))
            fontstatsexplosionbonusD = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '=', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+w+MENU_OFFSETX_ARROW*2, MENU_STARTY)))
            fontstatsscoreval = self.font_manager.add(Font(FontNames.STATS_ROUNDSCORE, InterfaceSettings.FONTSTYLE, 24, player.stats_scoreroundprev, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+w+MENU_OFFSETX_ARROW*3, MENU_STARTY)))
        else:
            fontstatsscoreval = self.font_manager.add(Font(FontNames.STATS_ROUNDSCORE, InterfaceSettings.FONTSTYLE, 24, player.stats_scoreroundprev, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontstatstotalscore = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Total Score', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        fontstatstotalscoreval = self.font_manager.add(Font(FontNames.STATS_BUBBLES, InterfaceSettings.FONTSTYLE, 24, player.score, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontstatsbubbles = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '# of Bubbles', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        fontstatsbubblesval = self.font_manager.add(Font(FontNames.STATS_BUBBLES, InterfaceSettings.FONTSTYLE, 24, player.stats_bubbles, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontstatsmult = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Max Multiplier', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        fontstatsmultval = self.font_manager.add(Font(FontNames.STATS_MAXMULTIPLIER, InterfaceSettings.FONTSTYLE, 24, player.stats_maxmultiplier, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontstatsexplosionsprev = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Explosions in Round', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        fontstatsexplosionsusedprevval = self.font_manager.add(Font(FontNames.STATS_EXPLOSIONSUSEDPREV, InterfaceSettings.FONTSTYLE, 24, GameSettings.PLAYER_EXPLOSIONS-player.stats_explosionsprev, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontstatsexplosions = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Total Explosions', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        fontstatsexplosionsusedval = self.font_manager.add(Font(FontNames.STATS_EXPLOSIONSUSED, InterfaceSettings.FONTSTYLE, 24, player.stats_explosions, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        SceneContext.instance.reset(player=player)

        MENU_STARTY += MENU_OFFSETY*2
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Press any key ...', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        self.timer_manager.add(SwitchSceneCommand(SceneNames.PLAY, onkeypress=True), 0)