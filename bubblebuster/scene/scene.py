from bubblebuster.image import ImageMan, ImageNames, BubbleImageMan
from bubblebuster.timer import TimerMan
from bubblebuster.group import CircleGroup, Group, GroupMan, GroupNames
from bubblebuster.font import FontMan
from bubblebuster.player import PlayerMan, PlayerNames, Player
from bubblebuster.settings import InterfaceSettings
from bubblebuster.sound import SoundMan
from bubblebuster.input import InputMan, Simulation
from bubblebuster.level import LevelMan, LevelNames
from bubblebuster.sprite.bubble import (
    BubbleMan, 
    IronBubble, 
    DelayBubble, 
    NukeBubble, 
    SlipperyBubble, 
    SpottedBubble, 
    TwinBubble
)
import bubblebuster.sprite as sp
import bubblebuster.collision as cl

from enum import Enum

class SceneNames(Enum):
    MENU = 1
    PLAY = 2
    OVER = 3
    RULES = 4
    SETTINGS = 5
    HIGHSCORES = 6
    SCENESWITCH = 7
    WEAPON = 8


class Scene:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.screen = game.screen
        self.image_manager = ImageMan()
        self.bubble_manager = BubbleMan()
        self.bubble_image_manager = BubbleImageMan()
        self.sprite_manager = sp.SpriteMan()
        self.boxsprite_manager = sp.BoxSpriteMan()
        self.input_manager = InputMan()
        self.group_manager = GroupMan()
        self.collisionpair_manager = cl.CollisionPairMan()
        self.font_manager = FontMan()
        self.timer_manager = TimerMan()
        self.sound_manager = SoundMan()
        self.simulation = Simulation()

        # one player man to rule them all
        self.player_manager = PlayerMan.create()

        # one level man to rule them all
        self.level_manager = LevelMan.create()

        # bubbles are ubiquitous !!
        #self.bubble_image_manager.add(ImageNames.BUBBLE, 'resources/bubble.png')
        list(map(lambda x: self.bubble_image_manager.add(getattr(ImageNames, '%sBUBBLE' % x.upper()), 'resources/bubble-%s.png' % x), InterfaceSettings.BUBBLECOLORS))
        self.image_manager.add(ImageNames.REDBUBBLE, 'resources/bubble-red.png')
        #self.bubble_image_manager.add(ImageNames.TESTMOUSE, 'resources/mouse.png')

        # all scenes have circle and wall groups
        self.circle_group = CircleGroup(GroupNames.CIRCLE)
        self.wall_group = Group(GroupNames.WALL)

        # add to groupssssss
        self.group_manager.add(self.circle_group)
        self.group_manager.add(self.wall_group)

        # add bubble types
        self.bubble_manager.add(IronBubble)
        self.bubble_manager.add(DelayBubble)
        self.bubble_manager.add(SlipperyBubble)
        self.bubble_manager.add(NukeBubble)
        self.bubble_manager.add(SpottedBubble)
        self.bubble_manager.add(TwinBubble)

        # the player
        PlayerMan.instance.add(
            Player(PlayerNames.PLAYERONE,
                   None # no weapon until selected
                   )
        )

        # add teh levels mate, for jimmy
        LevelMan.instance.add(LevelNames.POINTS)
        LevelMan.instance.add(LevelNames.TIME)
        LevelMan.instance.add(LevelNames.MULTIPLIER)
        LevelMan.instance.add(LevelNames.SNIPER)

        # all scenes have walls
        SCREEN_WIDTH, SCREEN_HEIGHT = (InterfaceSettings.SCREEN_WIDTH, InterfaceSettings.SCREEN_HEIGHT)
        self.wall_left = self.boxsprite_manager.add_wall_sprite(sp.LineSpriteNames.WALL_LEFT, (0, 0), (0, SCREEN_HEIGHT), color=(255, 0, 0), width=2)
        self.wall_right = self.boxsprite_manager.add_wall_sprite(sp.LineSpriteNames.WALL_RIGHT, (SCREEN_WIDTH-2, 0), (SCREEN_WIDTH-2, SCREEN_HEIGHT), color=(0, 255, 0), width=2)
        self.wall_top = self.boxsprite_manager.add_wall_sprite(sp.LineSpriteNames.WALL_TOP, (0, 0), (SCREEN_WIDTH, 0), color=(0, 255, 255), width=2)
        self.wall_bottom = self.boxsprite_manager.add_wall_sprite(sp.LineSpriteNames.WALL_BOTTOM, (0, SCREEN_HEIGHT-2), (SCREEN_WIDTH, SCREEN_HEIGHT-2), color=(255, 255, 0), width=2)
        
        self.wall_group.add(self.wall_left)
        self.wall_group.add(self.wall_right)
        self.wall_group.add(self.wall_top)
        self.wall_group.add(self.wall_bottom)

    def _init(self):
        raise NotImplementedError("this is an abstract class")

    def update(self, current_time):
        raise NotImplementedError("this is an abstract class")

    def draw(self):
        raise NotImplementedError("this is an abstract class")

    def transition(self):
        ImageMan.set_active(self.image_manager)
        BubbleMan.set_active(self.bubble_manager)
        BubbleImageMan.set_active(self.bubble_image_manager)
        sp.SpriteMan.set_active(self.sprite_manager)
        sp.BoxSpriteMan.set_active(self.boxsprite_manager)
        InputMan.set_active(self.input_manager)
        GroupMan.set_active(self.group_manager)
        cl.CollisionPairMan.set_active(self.collisionpair_manager)
        FontMan.set_active(self.font_manager)
        TimerMan.set_active(self.timer_manager)
        SoundMan.set_active(self.sound_manager)

    def handle(self, player=None):
        raise NotImplementedError("this is an abstract class")



class SceneOver(Scene):
    def __init__(self, name, game):
        super().__init__(name, game)

    def update(self):
        pass

    def draw(self):
        pass

    def handle(self, player=None):
        pass

