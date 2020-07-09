from bubblebuster.sound import SoundNames
from bubblebuster.sprite import CircleFactory
from bubblebuster.font import FontNames, Font
from bubblebuster.input import MouseClickObserver, MouseHoverHighlightObserver
from bubblebuster.settings import InterfaceSettings
from bubblebuster.collision import CollisionRectPair
import bubblebuster.scene.scene as sc


class SceneRules(sc.Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

        SCREEN_WIDTH, SCREEN_HEIGHT = (InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT)

        # zounds
        self.sound_manager.add_music(SoundNames.MUSICMENU, 'resources/settings_bubbles.wav')
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')
        self.font_manager.add(Font(FontNames.MENUTITLE, 
                                   InterfaceSettings.FONTSTYLE,
                                   72, 
                                   'How to Play', 
                                   InterfaceSettings.FONTCOLOR, 
                                   (InterfaceSettings.SCREEN_WIDTH//7, InterfaceSettings.SCREEN_HEIGHT//10)
                              )
        )


        # make some bubbles
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(10,
                                       max_xy=(InterfaceSettings.SCREEN_WIDTH,
                                               InterfaceSettings.SCREEN_HEIGHT),
                                       max_h=250
        )

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)

        MENU_STARTX = SCREEN_WIDTH // 8
        MENU_STARTY = SCREEN_HEIGHT // 3
        MENU_OFFSETY = 45
        MENU_OFFSETX = 300
        MENU_OFFSETX_ARROW = 50

        descriptionA = 'Click to spend explosions and pop all the bubbles'
        descriptionB = 'Left click for cheap small booms, right click for expensive big booms!'
        descriptionC = 'Earn bonus for blowing up stacked bubbles'
        descriptionD = 'Get more points for popping smaller bubbles'

        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, descriptionA, InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, descriptionB, InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, descriptionC, InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY
        self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 16, descriptionD, InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        #self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Left Mouse Click', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        #self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Small Explosion', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        #MENU_STARTY += MENU_OFFSETY
        #self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Right Mouse Click', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))
        #self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 32, 'Large Explosion', InterfaceSettings.FONTCOLOR, (MENU_STARTX+MENU_OFFSETX, MENU_STARTY)))

        MENU_STARTY += MENU_OFFSETY + 100
        fontmenu = self.font_manager.add(Font(FontNames.NULL, InterfaceSettings.FONTSTYLE, 24, 'Back to Menu', InterfaceSettings.FONTCOLOR, (MENU_STARTX, MENU_STARTY)))

        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontmenu, None))
        self.input_manager.lmouse.attach(MouseClickObserver(fontmenu, sc.SceneNames.MENU))

    def update(self):
        # font
        self.font_manager.update()

        # sprites
        self.boxsprite_manager.update()

        # input
        self.input_manager.update(self.game)

        # collisions
        self.collisionpair_manager.process()

        # scene transition
        sc.SceneMan.instance.update()

    def draw(self):
        self.background.draw(self.screen)
        self.boxsprite_manager.draw(self.screen)
        self.font_manager.draw(self.screen)

    def handle(self):
        musicmenu = self.sound_manager.find(SoundNames.MUSICMENU)
        musicmenu.play()

