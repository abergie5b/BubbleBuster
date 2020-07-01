from bubblebuster.link import LinkMan, Link
from bubblebuster.settings import GameSettings


class Level(Link):
    def __init__(self):
        super().__init__()
        self.bubbles = 0
        self.bubble_maxh = 0
        self.bubble_popdelay = 0
        self.bubble_maxdelta = 0
        self.time = 0


class ActiveLevel(Level):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.bubbles = GameSettings.NUMBER_OF_BUBBLES
        self.bubble_maxh = GameSettings.BUBBLE_MAXH
        self.bubble_popdelay = GameSettings.BUBBLEPOPDELAY
        self.bubble_maxdelta = GameSettings.BUBBLE_MAXDELTA
        self.time = 60

        self.max_bubbles = GameSettings.NUMBER_OF_BUBBLES
        self.max_bubbl_maxh = GameSettings.BUBBLE_MAXH
        self.max_time = 60

    def advance(self):
        self.bubbles = self.max_bubbles + self.level * 5
        self.bubble_maxh = self.bubble_maxh - self.level * 5
        self.time = self.max_time - self.level * 5
        self.level += 1

    def reset(self):
        self.level = 1
        self.bubbles = self.max_bubbles
        self.bubble_maxh = self.max_bubbl_maxh
        self.time = self.max_time


class LevelMan(LinkMan):
    def compare(self, a, b):
        return a.name == b

    def add(self, name, data):
        image = Level(name, data)
        self.base_add(image)

    def find(self, image):
        return self.base_find(image)

    @staticmethod
    def set_active(manager):
        LevelMan.instance = manager

