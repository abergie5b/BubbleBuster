from bubblebuster.link import LinkMan, Link
from bubblebuster.settings import GameSettings
import bubblebuster.player as pl

from enum import Enum
from random import randint

class LevelNames(Enum):
    ACTIVE = 1
    POINTS = 2
    TIME = 3
    SNIPER = 4
    MULTIPLIER = 5


class Level(Link):
    def __init__(self, name):
        super().__init__()
        self.name = name

        self.level = 1
        self.bubbles = GameSettings.NUMBER_OF_BUBBLES
        self.bubble_maxh = GameSettings.BUBBLE_MAXH
        self.bubble_popdelay = GameSettings.BUBBLEPOPDELAY
        self.bubble_maxdelta = GameSettings.BUBBLE_MAXDELTA
        self.time = 60

        self.max_bubbles = GameSettings.NUMBER_OF_BUBBLES
        self.max_bubbl_maxh = GameSettings.BUBBLE_MAXH
        self.max_time = 60

        # back pointer
        self.player = pl.PlayerMan.instance.find(pl.PlayerNames.PLAYERONE)

        # state
        self.is_active = False
        self.is_complete = False
        self.defeat = False

    def update(self):
        '''
        define win /lose condition for level here
        '''
        if self.bubbles <= 0:
            self.is_complete = True
        if not self.player.weapon.ammo and not self.is_complete:
            self.defeat = True

    def advance(self):
        self.level += 1
        self.is_complete = False
        self.defeat = False
        self.is_active = False

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
    def __init__(self):
        super().__init__(LevelNames.ACTIVE)

    def advance(self):
        self.bubbles = self.max_bubbles + self.level * 2
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 2
        self.time = self.max_time - self.level * 2
        super().advance()


class PointsLevel(Level):
    '''
    get a certain number of points
    '''
    def __init__(self):
        super().__init__(LevelNames.POINTS)
        self.target_score = 1000

    def _update(self):
        if self.player.score >= self.target_score:
            self.is_complete = True
        # no defeat condition

    def advance(self):
        self.bubbles = self.max_bubbles + self.level * 2
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 2
        self.time = self.max_time - self.level * 2
        super().advance()


class TimeLevel(Level):
    '''
    destroy all the bubbles before the time limit
    '''
    def __init__(self):
        super().__init__(LevelNames.TIME)
        self.target_time = 1000
        self.target_bubbles = 10

    def _update(self):
        if self.bubbles <= 0:
            self.is_complete = True
        if (self.target_time <= 0 or not self.player.weapon.ammo) and not self.is_complete:
            self.defeat = True
    
    def advance(self):
        self.bubbles = self.max_bubbles + self.level * 2
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 2
        self.time = self.max_time - self.level * 2
        super().advance()


class SniperLevel(Level):
    '''
    destroy all the bubbles before the time limit
    '''
    def __init__(self):
        super().__init__(LevelNames.SNIPER)
        self.target_time = 1000
        self.target_bubbles = 10

    def _update(self):
        if self.bubbles <= 0:
            self.is_complete = True
        if (self.target_time <= 0 or not self.player.weapon.ammo) and not self.is_complete:
            self.defeat = True
    
    def advance(self):
        self.bubbles = self.max_bubbles + self.level * 2
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 2
        self.time = self.max_time - self.level * 2
        super().advance()


class MultiplierLevel(Level):
    '''
    get a high enough multiplier to pass the level
    '''
    def __init__(self):
        super().__init__(LevelNames.MULTIPLIER)
        self.target_multiplier = 10

    def _update(self):
        if self.player.stats_maxmultiplier >= self.target_multiplier:
            self.is_complete = True
        # no defeat

    def advance(self):
        self.bubbles = self.max_bubbles + self.level * 2
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 2
        self.time = self.max_time - self.level * 2
        super().advance()


class LevelMan(LinkMan):
    instance = None

    @staticmethod
    def create():
        if not LevelMan.instance:
            LevelMan.instance = LevelMan.__new__(LevelMan)
            LevelMan.instance.current_level = None
            LevelMan.instance.head = None
            LevelMan.instance.length = 0
        return LevelMan.instance

    def __init__(self):
        raise NotImplementedError('this is a singleton class')

    def compare(self, a, b):
        return a.name == b

    def update(self):
        head = self.head
        while head:
            if head.is_active:
                head.update()
            head = head.next

    def remove(self, level):
        self.base_remove(level)

    def add(self, name):
        if name == LevelNames.ACTIVE:
            level = ActiveLevel()
        elif name == LevelNames.POINTS:
            level = PointsLevel()
        elif name == LevelNames.TIME:
            level = TimeLevel()
        elif name == LevelNames.MULTIPLIER:
            level = MultiplierLevel()
        elif name == LevelNames.SNIPER:
            level = SniperLevel()
        self.base_add(level)
        return level

    def add_level(self, level):
        self.base_add(level)
        return level

    def find(self, image):
        return self.base_find(image)

    def reset(self):
        head = self.head
        while head:
            head.is_active = False
            head.reset()
            head = head.next
        self.current_level = self.get_random()

    def advance(self):
        head = self.head
        while head:
            head.advance()
            head = head.next
        self.current_level = self.get_random()
        self.current_level.is_active = True
        #self.current_level.player = pl.PlayerMan.instance.find(pl.PlayerNames.PLAYERONE)
        
