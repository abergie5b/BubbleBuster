from bubblebuster.link import LinkMan, Link
from bubblebuster.settings import GameSettings

from enum import Enum

class LevelNames(Enum):
    ACTIVE = 1
    POINTS = 2
    TIME = 3


class Level(Link):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.bubbles = 0
        self.bubble_maxh = 0
        self.bubble_popdelay = 0
        self.bubble_maxdelta = 0
        self.time = 0

        self.max_bubbles = 0
        self.max_bubbl_maxh = 0
        self.max_time = 0

        # back pointer
        self.player = None

        # state
        self.is_complete = False
        self.defeat = False

    def update(self):
        '''
        define win /lose condition for level here
        '''
        # simple level default just destroy all bubbles
        if self.bubbles <= 0:
            self.is_complete = True
        if not self.player.weapon.ammo and not self.is_complete:
            self.defeat = True

    def advance(self):
        '''
        generic advance for moving to the next level
        when the next level is the same type of level
        '''
        self.bubbles = self.max_bubbles + self.level * 5
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 5
        self.time = self.max_time - self.level * 5
        self.level += 1
        self.is_complete = False
        self.defeat = False

    def reset(self):
        '''
        reset the level after game over
        '''
        self.level = 1
        self.bubbles = self.max_bubbles
        self.bubble_maxh = self.max_bubbl_maxh
        self.time = self.max_time
        self.is_complete = False
        self.defeat = False

    def transition(self, level):
        '''
        transition to a different type of level
        with a different win condition
        '''
        self.bubbles = level.bubbles
        self.bubble_maxh = level.bubble_maxh
        self.bubble_popdelay = level.bubble_popdelay
        self.bubble_maxdelta = level.bubble_maxdelta
        self.time = level.time

        self.max_bubbles = level.max_bubbles
        self.max_bubbl_maxh = level.bubble_maxh
        self.max_time = level.max_time

        self.is_complete = level.is_complete
        self.defeat = level.defeat


class ActiveLevel(Level):
    '''
    generic level (destroy all bubbles)
    '''
    def __init__(self, name):
        super().__init__(name)
        self.level = 1
        self.bubbles = GameSettings.NUMBER_OF_BUBBLES
        self.bubble_maxh = GameSettings.BUBBLE_MAXH
        self.bubble_popdelay = GameSettings.BUBBLEPOPDELAY
        self.bubble_maxdelta = GameSettings.BUBBLE_MAXDELTA
        self.time = 60

        # if gamesettings changes, have to update this, not ideal
        self.max_bubbles = GameSettings.NUMBER_OF_BUBBLES
        self.max_bubbl_maxh = GameSettings.BUBBLE_MAXH
        self.max_time = 60


class PointsLevel(Level):
    '''
    get a certain number of points
    '''
    def __init__(self, name):
        super().__init__(name)
        self.target_score = 1000

    def update(self):
        if self.player.score >= self.target_score:
            self.is_complete = True
        # no defeat condition


class TimeLevel(Level):
    '''
    destroy as many bubbles as you can within the time limit
    '''
    def __init__(self, name):
        super().__init__(name)
        self.target_time = 1000

    def update(self):
        if self.target_time <= 0:
            self.is_complete = True
        # no defeat
    

class MultiplierLevel(Level):
    '''
    get a high enough multiplier to pass the level
    '''
    def __init__(self, name):
        super().__init__(name)
        self.target_multiplier = 10

    def update(self):
        if self.player.stats_maxmultiplier >= self.target_multiplier:
            self.is_complete = True
        # no defeat


class LevelMan(LinkMan):
    instance = None
    def __init__(self):
        super().__init__()
        LevelMan.instance = self

    def compare(self, a, b):
        return a.name == b

    def update(self):
        head = self.head
        while head:
            head.update()
            head = head.next

    def remove(self, level):
        self.base_remove(level)

    def add(self, name):
        if name == LevelNames.ACTIVE:
            level = ActiveLevel(name)
        elif name == LevelNames.POINTS:
            level = PointsLevel(name)
        elif name == LevelNames.TIME:
            level = TimeLevel(name)
        self.base_add(level)
        return level

    def add_level(self, level):
        self.base_add(level)
        return level

    def find(self, image):
        return self.base_find(image)

    @staticmethod
    def set_active(manager):
        LevelMan.instance = manager

