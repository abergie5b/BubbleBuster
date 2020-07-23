from bubblebuster.link import LinkMan, Link
import bubblebuster.level as le

from enum import Enum


class Hint(Link):
    def __init__(self, hint):
        super().__init__()
        self.hint = hint

    def __repr__(self):
        return 'Hint: %s' % self.hint


class HintMan(LinkMan):
    instance = None

    @staticmethod
    def create():
        if not HintMan.instance:
            HintMan.instance = HintMan.__new__(HintMan)
            HintMan.instance.current_hint = None
            HintMan.instance.head = None
            HintMan.instance.length = 0
            HintMan.instance.init()
        return HintMan.instance

    def __init__(self):
        raise NotImplementedError('this is a singleton class')

    def init(self):
        self.add("Try to complete the objective with as few explosions as possible!")
        self.add("The time elapsed during each round contributes to the score!")

    def compare(self, a, b):
        return a.name == b

    def remove(self, hint):
        self.base_remove(hint)

    def add(self, hint):
        hint = Hint(hint)
        self.base_add(hint)
        return hint

    def find(self, image):
        return self.base_find(image)

    def update(self):
        raise ImplementationError("HintMan does not get updated")

    def draw(self):
        raise ImplementationError("HintMan does not get drawn")

