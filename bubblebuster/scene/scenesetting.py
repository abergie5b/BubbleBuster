from bubblebuster.sound import SoundNames, Music
from bubblebuster.sprite import CircleFactory
from bubblebuster.font import FontNames, Font
from bubblebuster.input import MouseClickObserver, MouseClickSettingsObserver, MouseHoverHighlightObserver
from bubblebuster.settings import InterfaceSettings, GameSettings
from bubblebuster.collision import CollisionRectPair
import bubblebuster.scene.scene as sc


class SceneSettings(sc.Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

        SCREEN_WIDTH, SCREEN_HEIGHT = (InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT)

        # zounds
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')
        self.sound_manager.add_music(SoundNames.MUSICMENU, 'resources/settings_bubbles.wav')

        # make some bubbles
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(10,
                                       max_xy=(SCREEN_WIDTH,
                                               SCREEN_HEIGHT),
                                       max_h=250
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
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Bubble Bust Delay', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        self.font_manager.add(Font(FontNames.BUBBLEPOPDELAY, InterfaceSettings.FONTSTYLE, 24, GameSettings.BUBBLEPOPDELAY, InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))
        bubblepopdelayup = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '+', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY)))
        bubblepopdelaydown = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, '-', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX+MENU_OFFSETX_ARROW, MENU_STARTY+20)))

        MENU_STARTY += MENU_OFFSETY
        fontmenu = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Back to Menu', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontmenu, None))
        self.input_manager.lmouse.attach(MouseClickObserver(fontmenu, sc.SceneNames.MENU))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(numberofbubblesup, 'NUMBER_OF_BUBBLES', FontNames.NUMBEROFBUBBLES, 10))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(numberofbubblesdown, 'NUMBER_OF_BUBBLES', FontNames.NUMBEROFBUBBLES, -10))

        self.input_manager.lmouse.attach(MouseClickSettingsObserver(bubblesmaxheightup, 'BUBBLE_MAXH', FontNames.BUBBLESMAXH, 10))
        self.input_manager.lmouse.attach(MouseClickSettingsObserver(bubblesmaxheightdown, 'BUBBLE_MAXH', FontNames.BUBBLESMAXH, -10))

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

    def handle(self):
        musicmenu = self.sound_manager.find(SoundNames.MUSICMENU)
        musicmenu.play()

