import bubblebuster.sprite as sp
import bubblebuster.collision as cl
import bubblebuster.highscores as hs
import bubblebuster.scene.scenecontext as sccxt
import bubblebuster.timer as ti
from bubblebuster.image import ImageMan, ImageNames, BubbleImageMan
from bubblebuster.timer import TimerMan
from bubblebuster.group import CircleGroup, Group, GroupMan, GroupNames
from bubblebuster.font import FontMan
from bubblebuster.player import PlayerMan
from bubblebuster.settings import InterfaceSettings, DEBUG
from bubblebuster.sound import SoundMan
from bubblebuster.input import InputMan, Simulation
from bubblebuster.level import LevelMan, HintMan
from bubblebuster.sprite.bubble import (
    BubbleMan, 
    IronBubble, 
    DelayBubble, 
    NukeBubble, 
    SlipperyBubble, 
    SpottedBubble, 
    TwinBubble
)
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

        # one high score to rule them all
        self.highscores = hs.HighScores()

        # one scene man to rule them all
        self.scene_manager = SceneMan.create()

        # one hint man to rule them all
        self.hint_manager = HintMan.create()

        # background
        background = self.image_manager.add(ImageNames.BEACHDIGITALBACKGROUND, 
                                            'resources/beach.png')
        # all scenes start with same background
        self.background = sp.Background(background)

        # bubbles are ubiquitous !!
        #self.bubble_image_manager.add(ImageNames.BUBBLE, 'resources/bubble.png')
        list(map(lambda x: self.bubble_image_manager.add(getattr(ImageNames, '%sBUBBLE' % x.upper()), 'resources/bubble-%s.png' % x), InterfaceSettings.BUBBLECOLORS))
        self.image_manager.add(ImageNames.REDBUBBLE, 'resources/bubble-red.png')

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
        SoundMan.set_active(self.sound_manager)
        TimerMan.set_active(self.timer_manager)

    def handle(self):
        raise NotImplementedError("this is an abstract class")


class SceneMan:
    instance = None
    @staticmethod
    def create():
        if not SceneMan.instance:
            SceneMan.instance = SceneMan.__new__(SceneMan)
            SceneMan.instance.head = None # SceneNames
            SceneMan.instance.prev = None # SceneNames
            SceneMan.instance.length = 0
        return SceneMan.instance

    def __init__(self):
        raise NotImplementedError('this is a singleton class')

    def set_scene(self, scenename):
        self.prev = self.head
        self.head = scenename
        self.length = 1

    def update(self):
        if self.head:
            head = self.head
            self.head = None # pop
            self.length = 0

            # clean up
            ti.TimerMan.instance.remove_all()

            sp.BoxSpriteMan.instance.remove_all_type(sp.SpriteTypes.BUBBLE)
            sp.BoxSpriteMan.instance.remove_all_type(sp.SpriteTypes.EXPLOSION)

            cl.CollisionPairMan.instance.remove_all_type(sp.SpriteTypes.BUBBLE)
            cl.CollisionPairMan.instance.remove_all_type(sp.SpriteTypes.EXPLOSION)

            if DEBUG:
                print('changing scene from %s to %s' % (self.prev, head))

            sccxt.SceneContext.instance.set_state(head)

    def remove(self, scene):
        self.head = None
        self.length = 0

