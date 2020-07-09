from bubblebuster.sound import SoundNames
from bubblebuster.font import FontNames, Font
from bubblebuster.settings import InterfaceSettings
from bubblebuster.input import MouseClickObserver, MouseHoverHighlightObserver, MouseClickExitObserver
from bubblebuster.sprite import CircleFactory
from bubblebuster.collision import CollisionRectPair
import bubblebuster.scene.scene as sc
import bubblebuster.image as im

class SceneMenu(sc.Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

        SCREEN_WIDTH, SCREEN_HEIGHT = (InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT)

        # zounds
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')
        self.sound_manager.add_music(SoundNames.MUSICMENU, 'resources/bubbling.wav')

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
                                   'Bubble Buster', 
                                   InterfaceSettings.FONTCOLOR, 
                                   (SCREEN_WIDTH//7, SCREEN_HEIGHT//6)
                              )
        )

        MENU_STARTX = SCREEN_WIDTH // 6
        MENU_STARTY = SCREEN_HEIGHT // 1.75
        MENU_OFFSETY = 45
        MENU_OFFSETX = 100

        fontplay = self.font_manager.add(Font(FontNames.PLAY, InterfaceSettings.FONTSTYLE, 32, 'Start Game', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontrules = self.font_manager.add(Font(FontNames.RULES, InterfaceSettings.FONTSTYLE, 32, 'How to Play', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontsettings = self.font_manager.add(Font(FontNames.SETTINGS, InterfaceSettings.FONTSTYLE, 32, 'Settings', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fonthighscores = self.font_manager.add(Font(FontNames.HIGHSCORES, InterfaceSettings.FONTSTYLE, 32, 'High Scores', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        fontexit = self.font_manager.add(Font(FontNames.EXIT, InterfaceSettings.FONTSTYLE, 32, 'Exit', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        self.input_manager.lmouse.attach(MouseClickObserver(fontplay, sc.SceneNames.WEAPON, None))
        self.input_manager.lmouse.attach(MouseClickObserver(fontrules, sc.SceneNames.RULES))
        self.input_manager.lmouse.attach(MouseClickObserver(fontsettings, sc.SceneNames.SETTINGS))
        self.input_manager.lmouse.attach(MouseClickObserver(fonthighscores, sc.SceneNames.HIGHSCORES))
        self.input_manager.lmouse.attach(MouseClickExitObserver(fontexit, None))

        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontplay, None))
        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontrules, None))
        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontsettings, None))
        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fonthighscores, None))
        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontexit, None))

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)

    def update(self):
        # input updates
        self.input_manager.update(self.game)

        # sprites
        self.boxsprite_manager.update()

        # collisions
        self.collisionpair_manager.process()

        # fonts ...
        self.font_manager.update()

        # scene transition
        sc.SceneMan.instance.update()

    def draw(self):
        self.background.draw(self.screen)

        self.boxsprite_manager.draw(self.screen)

        self.font_manager.draw(self.screen)

    def handle(self):
        musicmenu = self.sound_manager.find(SoundNames.MUSICMENU)
        musicmenu.play()
