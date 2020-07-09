from bubblebuster.link import LinkMan, Link
from bubblebuster.settings import GameSettings
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
        self.target_time = self.max_time = 30000

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
        return ''

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
        self.description = self.get_desc()
        self.hint = self.get_hint()
        ti.TimerMan.instance.remove(ti.TimeEventNames.SETGAMEOVER)


class PointsLevel(Level):
    '''
    get a certain number of points
    '''
    def __init__(self):
        self.target_score = 25 # should be a GameSetting
        self.target_time = 0
        super().__init__(LevelNames.POINTS)
        # not used this level
        self.target_bubbles = self.bubbles

    def get_desc(self):
        return 'Get %d points!' % self.target_score

    def get_hint(self):
        return 'You might have to use multipliers wisely!'

    def update(self):
        if self.player.stats_scoreround >= self.target_score:
            self.is_complete = True
        # no defeat condition

    def advance(self):
        self.target_score = 25 + self.level * 2
        self.bubbles = self.max_bubbles + self.level * 2
        self.target_bubbles = self.bubbles
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 2
        self.time = self.max_time - self.level * 2
        super().advance()


class TimeLevel(Level):
    '''
    destroy all the bubbles before the time limit
    '''
    def __init__(self):
        self.target_bubbles = 10 # should be a GameSetting
        super().__init__(LevelNames.TIME)

    def get_desc(self):
        return 'Pop %d bubbles in %d seconds!' % (self.target_bubbles, int(self.target_time//1000))

    def get_hint(self):
        return 'Move quickly! Watch the clock!'

    def update(self):
        if self.target_bubbles <= 0:
            self.is_complete = True
        if not self.player.weapon.ammo and not self.is_complete:
            self.defeat = True
    
    def advance(self):
        self.bubbles = self.max_bubbles + self.level * 2
        self.target_bubbles = 10 + self.level * 2
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 2
        self.target_time = max(self.max_time - self.level * 1000, 10000)
        super().advance()



class SniperLevel(Level):
    '''
    destroy all the bubbles before the time limit
    '''
    def __init__(self):
        self.target_bubbles = 10 # should be a GameSetting
        super().__init__(LevelNames.SNIPER)

    def get_desc(self):
        return 'Pop %d bubbles in %d seconds using the sniper!' % (self.target_bubbles, int(self.target_time/1000))

    def get_hint(self):
        return 'This round gives extra points. Show off your skills!'

    def update(self):
        if self.target_bubbles <= 0:
            self.is_complete = True
        if not self.player.weapon.ammo and not self.is_complete:
            self.defeat = True
    
    def advance(self):
        self.target_bubbles = 10 + self.level * 2
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 2
        self.target_time = max(self.max_time - self.level * 1000, 10000)
        super().advance()


class MultiplierLevel(Level):
    '''
    get a high enough multiplier to pass the level
    '''
    def __init__(self):
        self.target_multiplier = 3
        self.target_time = 0
        super().__init__(LevelNames.MULTIPLIER)
        self.target_bubbles = self.bubbles

    def get_desc(self):
        return 'Get a %dx pop multiplier!' % (self.target_multiplier)

    def get_hint(self):
        return 'Take your time and wait for the bubbles to group up!'

    def update(self):
        if self.player.stats_maxmultiplierround >= self.target_multiplier:
            self.is_complete = True
        if (not self.target_bubbles or not self.player.weapon.ammo) and not self.is_complete:
            self.defeat = True

    def advance(self):
        self.target_multiplier += 1
        self.bubbles = self.max_bubbles + self.level * 2
        self.target_bubbles = self.bubbles
        self.bubble_maxh = self.max_bubbl_maxh - self.level * 2
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

    def init(self):
        self.head = None
        self.add(LevelNames.POINTS)
        self.add(LevelNames.TIME)
        self.add(LevelNames.MULTIPLIER)
        self.add(LevelNames.SNIPER)

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
        if name == LevelNames.POINTS:
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

        # do this
        GameSettings.BUBBLE_PROCPROBA += 0.01

        # clean up
        ti.TimerMan.instance.remove_all()
        sp.BoxSpriteMan.instance.remove_all_type(sp.SpriteTypes.BUBBLE)
        