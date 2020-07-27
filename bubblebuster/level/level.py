import bubblebuster.link as li
import bubblebuster.settings as se
import bubblebuster.player as pl
import bubblebuster.timer as ti
import bubblebuster.sprite as sp

from enum import Enum

class LevelNames(Enum):
    ACTIVE = 1
    POINTS = 2
    TIME = 3
    SNIPER = 4
    MULTIPLIER = 5


class Level(li.Link):
    def __init__(self, name):
        '''
        define base class for Levels
        '''
        super().__init__()
        self.name = name

        self.level = 1

        # the number of bubbles generated on this level
        self.bubbles = se.GameSettings.NUMBER_OF_BUBBLES

        # maximum bubble height
        self.bubble_maxh = se.GameSettings.BUBBLE_MAXH

        # duration before bubble pops after click
        self.bubble_popdelay = se.GameSettings.BUBBLEPOPDELAY

        # maximum bubble velocity
        self.bubble_maxdelta = se.GameSettings.BUBBLE_MAXDELTA

        # the number of bubbles generated on this level
        self.max_bubbles = se.GameSettings.NUMBER_OF_BUBBLES

        # maximum bubble height
        self.max_bubbl_maxh = se.GameSettings.BUBBLE_MAXH

        self.time = 60
        self.target_time = self.max_time = 25000

        # back pointer
        self.player = pl.PlayerMan.instance.find(pl.PlayerNames.PLAYERONE)

        # state
        self.is_active = False
        self.is_complete = False
        self.defeat = False

        # more stuff
        self.description = self.get_desc()
        self.hint = self.get_hint()

    def get_desc(self):
        return ''

    def get_hint(self):
        return HintMan.instance.get_random()

    def update(self):
        '''
        define win /lose condition for level here
        '''
        if self.bubbles <= 0:
            self.is_complete = True
        if not self.player.weapon.ammo and not self.is_complete:
            self.defeat = True

    def advance(self):
        '''
        define how the level scales here
        '''
        self.level += 1
        self.is_complete = False
        self.defeat = False
        self.is_active = False
        self.description = self.get_desc()
        self.hint = self.get_hint()

        # update the bubble velocity
        self.bubble_maxdelta += se.GameSettings.BUBBLE_MAXDELTA_DELTA

        # redundant methinks (handled in scene.py)
        ti.TimerMan.instance.remove(ti.TimeEventNames.SETGAMEOVER)

