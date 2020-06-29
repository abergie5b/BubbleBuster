from bubblebuster.scene import Scene

from bubblebuster.sprite import CircleFactory, LineSpriteNames, LineSprite
from bubblebuster.sound import SoundNames, Music
from bubblebuster.scene import Scene, SceneContext, SceneNames
from bubblebuster.settings import InterfaceSettings
from bubblebuster.collision import CollisionRectPair
from bubblebuster.font import Font, FontNames
from bubblebuster.timer import SwitchSceneCommand
from bubblebuster.settings import InterfaceSettings, GameSettings
from bubblebuster.input import MouseClickObserver, LMouseClickRectObserver
from bubblebuster.ui import WeaponCarousel
from bubblebuster.weapon import Finger, Thumb, Hand, WeaponNames
from bubblebuster.player import Player, PlayerMan, PlayerNames
from bubblebuster.font import FontNames, Font

import pygame


class SceneWeapon(Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

        # zounds
        self.sound_manager.add(SoundNames.BUBBLEPOP, 'resources/bubble_pop.wav')

        # font
        MENU_STARTX = InterfaceSettings.SCREEN_WIDTH - InterfaceSettings.SCREEN_WIDTH // 4
        MENU_STARTY = InterfaceSettings.SCREEN_HEIGHT - InterfaceSettings.SCREEN_HEIGHT // 6
        self.font_manager.instance.add(Font(FontNames.PLAY,
                                       InterfaceSettings.FONTSTYLE,
                                       32,
                                       '',
                                       InterfaceSettings.FONTCOLOR,
                                       (MENU_STARTX, MENU_STARTY))
                                  )

        # make some bubbles
        circle_factory = CircleFactory(self.circle_group, self.boxsprite_manager)
        circle_factory.generate_random(10,
                                       max_xy=(InterfaceSettings.SCREEN_WIDTH,
                                               InterfaceSettings.SCREEN_HEIGHT),
                                       max_h=100
                                       )

        # collision pairs
        self.collisionpair_manager.add_groups(self.wall_group, self.circle_group, CollisionRectPair)

        # make a carousel
        carousel = WeaponCarousel((InterfaceSettings.SCREEN_WIDTH//8, InterfaceSettings.SCREEN_HEIGHT//8),
                                  (InterfaceSettings.SCREEN_WIDTH-InterfaceSettings.SCREEN_WIDTH//4, InterfaceSettings.SCREEN_HEIGHT//2),
                                  windows=3
        )

        # make the player, pass to scene play
        # do it
        self.player = Player(PlayerNames.PLAYERONE,
                             None, # no weapon until selected
                             GameSettings.NUMBER_OF_BUBBLES
                             )

        # get the available weapons from player / profile object
        # create manually for now
        finger = Finger(WeaponNames.FINGER)
        thumb = Thumb(WeaponNames.THUMB)
        hand = Hand(WeaponNames.HAND)

        carousel.add_weapons([finger, thumb, hand])

        self.boxsprite_manager.add_boxgroup(carousel)

        # attach this
        carousel.attach(self.player, LMouseClickRectObserver)
        self.player = self.player_manager.add(self.player)


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

    def draw(self):
        self.boxsprite_manager.draw(self.screen)

        self.font_manager.draw(self.screen)

        self.sprite_manager.draw(self.screen)

    def handle(self, player=None):
        assert(self.player)
