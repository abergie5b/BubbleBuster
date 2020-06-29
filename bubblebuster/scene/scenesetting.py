from bubblebuster.scene import Scene, SceneNames
from bubblebuster.sound import SoundNames, Music
from bubblebuster.sprite import CircleFactory
from bubblebuster.font import FontNames, Font
from bubblebuster.input import MouseClickObserver, MouseClickSettingsObserver, MouseHoverHighlightObserver
from bubblebuster.settings import InterfaceSettings, GameSettings
from bubblebuster.collision import CollisionRectPair


class SceneSettings(Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

        SCREEN_WIDTH, SCREEN_HEIGHT = (InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT)

        # zounds
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')

        # make some bubbles
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(10,
                                       max_xy=(SCREEN_WIDTH,
                                               SCREEN_HEIGHT),
                                       max_h=100
        )

        self.font_manager.add(Font(FontNames.MENUTITLE, 
                                   InterfaceSettings.FONTSTYLE,
                                   72, 
                                   'Settings', 
                                   InterfaceSettings.FONTCOLOR, 
                                   (SCREEN_WIDTH//7, SCREEN_HEIGHT//12)
                              )
        )

        MENU_STARTX = SCREEN_WIDTH // 4
        MENU_STARTY = SCREEN_HEIGHT // 3
        MENU_OFFSETY = 45
        MENU_OFFSETX = 350
        MENU_OFFSETX_ARROW = 75

        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '# of Bubbles', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.NUMBEROFBUBBLES, InterfaceSettings.FONTSTYLE, 24, GameSettings.NUMBER_OF_BUBBLES, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        numberofbubblesup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '+', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        numberofbubblesdown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '-', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+20)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Bubble Max Height', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.BUBBLESMAXH, InterfaceSettings.FONTSTYLE, 24, GameSettings.BUBBLE_MAXH, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        bubblesmaxheightup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '+', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        bubblesmaxheightdown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '-', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+20)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, '# of Explosions', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.NUMBEROFEXPLOSIONS, InterfaceSettings.FONTSTYLE, 24, GameSettings.PLAYER_EXPLOSIONS, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        numberofexplosionsup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '+', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        numberofexplosionsdown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '-', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+20)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Explosion Duration', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.EXPLOSIONDURATION, InterfaceSettings.FONTSTYLE, 24, GameSettings.EXPLOSION_MAX_LIVES, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        explosiondurationup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '+', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        explosiondurationdown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '-', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+20)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Explosion Radius Delta', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.EXPLOSIONRADIUS, InterfaceSettings.FONTSTYLE, 24, GameSettings.EXPLOSION_RADIUS, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        explosionradiusup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '+', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        explosionradiusdown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '-', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+20)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Bubble Bust Delay', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.BUBBLEPOPDELAY, InterfaceSettings.FONTSTYLE, 24, GameSettings.BUBBLEPOPDELAY, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        bubblepopdelayup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '+', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        bubblepopdelaydown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '-', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+20)))

        MENU_STARTY += MENU_OFFSETY
        fontmenu = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Back to Menu', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontmenu, None))
        self.input_manager.lmouse.attach(MouseClickObserver(fontmenu, SceneNames.MENU))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(numberofbubblesup, 'NUMBER_OF_BUBBLES', FontNames.NUMBEROFBUBBLES, 10))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(numberofbubblesdown, 'NUMBER_OF_BUBBLES', FontNames.NUMBEROFBUBBLES, -10))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(bubblesmaxheightup, 'BUBBLE_MAXH', FontNames.BUBBLESMAXH, 10))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(bubblesmaxheightdown, 'BUBBLE_MAXH', FontNames.BUBBLESMAXH, -10))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(numberofexplosionsup, 'PLAYER_EXPLOSIONS', FontNames.NUMBEROFEXPLOSIONS, 1))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(numberofexplosionsdown, 'PLAYER_EXPLOSIONS', FontNames.NUMBEROFEXPLOSIONS, -1))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(explosiondurationup, 'EXPLOSION_MAX_LIVES', FontNames.EXPLOSIONDURATION, 5))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(explosiondurationdown, 'EXPLOSION_MAX_LIVES', FontNames.EXPLOSIONDURATION, -5))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(explosionradiusup, 'EXPLOSION_RADIUS', FontNames.EXPLOSIONRADIUS, 1))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(explosionradiusdown, 'EXPLOSION_RADIUS', FontNames.EXPLOSIONRADIUS, -1))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(bubblepopdelayup, 'BUBBLEPOPDELAY', FontNames.BUBBLEPOPDELAY, 10))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(bubblepopdelaydown, 'BUBBLEPOPDELAY', FontNames.BUBBLEPOPDELAY, -10))

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)


    def update(self):
        # font
        self.font_manager.update()

        # sprites
        self.boxsprite_manager.update()

        # input
        self.input_manager.update(self.game)

        # collisions
        self.collisionpair_manager.process()

    def draw(self):
        self.boxsprite_manager.draw(self.screen)
        self.font_manager.draw(self.screen)

    def handle(self, player=None):
        musicmenu = Music(SoundNames.MUSICMENU, 'resources/settings_bubbles.wav')
        musicmenu.play()

