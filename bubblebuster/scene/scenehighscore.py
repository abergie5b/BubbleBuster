from bubblebuster.sound import SoundNames
import bubblebuster.scene.scene as sc
import bubblebuster.font as ft
import bubblebuster.settings as st
import bubblebuster.input as inp
import bubblebuster.highscores as hs
import bubblebuster.sprite as sp
import bubblebuster.collision as cl

class SceneHighScores(sc.Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

        # zounds
        self.sound_manager.add_music(SoundNames.MUSICMENU, 'resources/settings_bubbles.wav')
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')

        # MAKE SOME BUBBLESSS
        circle_factory = sp.CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(10,
                                       max_xy=(st.InterfaceSettings.SCREEN_WIDTH,
                                               st.InterfaceSettings.SCREEN_HEIGHT),
                                       max_h=250
                                       )
        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, cl.CollisionRectPair)

        self.font_manager.add(ft.Font(ft.FontNames.MENUTITLE, 
                                      st.InterfaceSettings.FONTSTYLE,
                                      72, 
                                      'High Scores', 
                                      st.InterfaceSettings.FONTCOLOR, 
                                      (st.InterfaceSettings.SCREEN_WIDTH//7, st.InterfaceSettings.SCREEN_HEIGHT//12)
                              )
        )

        MENU_STARTX_ORIG = MENU_STARTX = st.InterfaceSettings.SCREEN_WIDTH // 8
        MENU_STARTY = st.InterfaceSettings.SCREEN_HEIGHT // 4
        MENU_ENDY = st.InterfaceSettings.SCREEN_HEIGHT - st.InterfaceSettings.SCREEN_HEIGHT // 6
        OFFSETX = 150
        OFFSETY = 25

        # load high scores 
        highscorejson = hs.HighScores.instance.load_all()

        if highscorejson:
            # columns for the table
            highscorejson['Player'] = {'score': 'Score',
                                       'maxmultiplier': 'MaxMultiplier',
                                       'bubbles': 'Bubbles',
                                       'explosions': 'Explosions'}
            self.make_highscore_tablerow('Player', highscorejson.pop('Player'), MENU_STARTX, OFFSETX, MENU_STARTY)
            MENU_STARTY += OFFSETY

            # player data
            for name, player in sorted(highscorejson.items(), key=lambda x: x[1]['score'], reverse=True)[:15]:
                self.make_highscore_tablerow(name, player, MENU_STARTX, OFFSETX, MENU_STARTY)
                MENU_STARTY += OFFSETY

        # back to menu button
        fontmenu = self.font_manager.add(ft.Font(ft.FontNames.NULL,
                                                 st.InterfaceSettings.FONTSTYLE,
                                                 24,
                                                 'Back to Menu',
                                                 st.InterfaceSettings.FONTCOLOR,
                                                 (st.InterfaceSettings.SCREEN_WIDTH // 8, MENU_ENDY))
                                         )

        self.input_manager.mousecursor.attach(inp.MouseHoverHighlightObserver(fontmenu, None))
        self.input_manager.lmouse.attach(inp.MouseClickObserver(fontmenu, sc.SceneNames.MENU))
    
    def make_highscore_tablerow(self, name, player, MENU_STARTX, OFFSETX, MENU_STARTY):
        self.font_manager.add(ft.Font(ft.FontNames.NULL,
                                      st.InterfaceSettings.FONTSTYLE,
                                      16,
                                      name,
                                      st.InterfaceSettings.FONTCOLOR,
                                      (MENU_STARTX, MENU_STARTY)
                                  ))
        MENU_STARTX += OFFSETX*3
        self.font_manager.add(ft.Font(ft.FontNames.NULL,
                                      st.InterfaceSettings.FONTSTYLE,
                                      16,
                                      player['score'],
                                      st.InterfaceSettings.FONTCOLOR,
                                      (MENU_STARTX, MENU_STARTY)
                                  ))
        MENU_STARTX += OFFSETX
        self.font_manager.add(ft.Font(ft.FontNames.NULL,
                                      st.InterfaceSettings.FONTSTYLE,
                                      16,
                                      player['maxmultiplier'],
                                      st.InterfaceSettings.FONTCOLOR,
                                      (MENU_STARTX, MENU_STARTY)
                                  ))
        MENU_STARTX += OFFSETX
        self.font_manager.add(ft.Font(ft.FontNames.NULL,
                                      st.InterfaceSettings.FONTSTYLE,
                                      16,
                                      player['bubbles'],
                                      st.InterfaceSettings.FONTCOLOR,
                                      (MENU_STARTX, MENU_STARTY)
                                  ))
        MENU_STARTX += OFFSETX
        self.font_manager.add(ft.Font(ft.FontNames.NULL,
                                      st.InterfaceSettings.FONTSTYLE,
                                      16,
                                      player['explosions'],
                                      st.InterfaceSettings.FONTCOLOR,
                                      (MENU_STARTX, MENU_STARTY)
                                  ))


    def update(self):
        # input updates
        self.input_manager.update(self.game)

        # sprites
        self.boxsprite_manager.update()

        # collisions
        self.collisionpair_manager.process()

        # fonts ...
        self.font_manager.update()

    def draw(self):
        self.boxsprite_manager.draw(self.screen)

        self.font_manager.draw(self.screen)

    def handle(self):
        musicmenu = self.sound_manager.find(SoundNames.MUSICMENU)
        musicmenu.play()

