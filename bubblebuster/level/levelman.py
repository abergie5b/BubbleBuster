import bubblebuster.link as li
import bubblebuster.level as le
import bubblebuster.settings as se
import bubblebuster.level.multiplierlevel as mule
import bubblebuster.level.sniperlevel as snle
import bubblebuster.level.pointslevel as pole
import bubblebuster.level.timelevel as tile


class LevelMan(li.LinkMan):
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
        self.add(le.LevelNames.POINTS)
        self.add(le.LevelNames.TIME)
        self.add(le.LevelNames.MULTIPLIER)
        self.add(le.LevelNames.SNIPER)

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
        if name == le.LevelNames.POINTS:
            level = pole.PointsLevel()
        elif name == le.LevelNames.TIME:
            level = tile.TimeLevel()
        elif name == le.LevelNames.MULTIPLIER:
            level = mule.MultiplierLevel()
        elif name == le.LevelNames.SNIPER:
            level = snle.SniperLevel()
        else:
            raise ValueError('invalid level %s' % name)
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
        se.GameSettings.BUBBLE_PROCPROBA += 0.01
