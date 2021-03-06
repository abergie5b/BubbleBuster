from bubblebuster.sprite import CircleFactory
from bubblebuster.sound import SoundNames
from bubblebuster.settings import InterfaceSettings
from bubblebuster.collision import CollisionRectPair
from bubblebuster.font import Font, FontNames
from bubblebuster.settings import InterfaceSettings, GameSettings
from bubblebuster.input import LMouseClickRectObserver, MouseHoverHighlightObserver, MouseClickObserver
from bubblebuster.ui import WeaponCarousel
from bubblebuster.weapon import Finger, Thumb, Hand, WeaponNames
from bubblebuster.player import Player, PlayerNames, PlayerMan
from bubblebuster.font import FontNames, Font
from bubblebuster.image import ImageNames
import bubblebuster.level as le
import bubblebuster.scene.scene as sc

import pygame


class SceneWeapon(sc.Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

        # images
        self.image_manager.add(ImageNames.FINGER, 'resources/finger.png')
        self.image_manager.add(ImageNames.THUMB, 'resources/thumb.png')
        self.image_manager.add(ImageNames.HAND, 'resources/hand.png')

        # zounds
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')

        # font
        MENU_STARTX = InterfaceSettings.SCREEN_WIDTH - InterfaceSettings.SCREEN_WIDTH // 4
        MENU_STARTY = InterfaceSettings.SCREEN_HEIGHT - InterfaceSettings.SCREEN_HEIGHT // 6
        fontplay = self.font_manager.instance.add(Font(FontNames.PLAY,
                                                  InterfaceSettings.FONTSTYLE,
                                                  32,
                                                  '',
                                                  InterfaceSettings.FONTCOLOR,
                                                  (MENU_STARTX, MENU_STARTY))
                                             )
        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontplay, None))


        # make a carousel
        carousel = WeaponCarousel((InterfaceSettings.SCREEN_WIDTH//8, InterfaceSettings.SCREEN_HEIGHT//8),
                                  (InterfaceSettings.SCREEN_WIDTH-InterfaceSettings.SCREEN_WIDTH//4, InterfaceSettings.SCREEN_HEIGHT//2),
                                  windows=3
        )

        # get the available weapons from player / profile object
        # create manually for now
        finger = Finger(WeaponNames.FINGER)
        thumb = Thumb(WeaponNames.THUMB)
        hand = Hand(WeaponNames.HAND)

        carousel.add_weapons([finger, thumb, hand])

        self.boxsprite_manager.add_boxgroup(carousel)

        # the player
        PlayerMan.instance.add(
            Player(PlayerNames.PLAYERONE,
                   None # no weapon until selected
                   )
        )

        # add teh levels mate, for jimmy
        le.LevelMan.instance.init()

        # lets do a random level
        le.LevelMan.instance.current_level = le.LevelMan.instance.get_random()
        le.LevelMan.instance.current_level.is_active = True

        # 
        carousel.attach(LMouseClickRectObserver)

        MENU_ENDY = InterfaceSettings.SCREEN_HEIGHT - InterfaceSettings.SCREEN_HEIGHT // 6
        # back to menu button
        fontmenu = self.font_manager.add(Font(FontNames.NULL,
                                                 InterfaceSettings.FONTSTYLE,
                                                 24,
                                                 'Back to Menu',
                                                 InterfaceSettings.FONTCOLOR,
                                                 (InterfaceSettings.SCREEN_WIDTH // 8, MENU_ENDY))
                                         )

        self.input_manager.mousecursor.attach(MouseHoverHighlightObserver(fontmenu, None))
        self.input_manager.lmouse.attach(MouseClickObserver(fontmenu, sc.SceneNames.MENU))

    def update(self):
        time = pygame.time.get_ticks()

        # input updates
        self.input_manager.update(self.game)

        # sprites
        self.boxsprite_manager.update()
        self.sprite_manager.update()

        # collisions
        self.collisionpair_manager.process()

        # fonts ...
        self.font_manager.update()

        # time
        self.timer_manager.update(self, time)

        # scene transition
        sc.SceneMan.instance.update()

    def draw(self):
        self.background.draw(self.screen)

        self.boxsprite_manager.draw(self.screen)

        self.font_manager.draw(self.screen)

        self.sprite_manager.draw(self.screen)

    def handle(self):

        # this is bad,
        # but need to set in case changed from scenesettings
        le.LevelMan.instance.current_level.bubbles = GameSettings.NUMBER_OF_BUBBLES

