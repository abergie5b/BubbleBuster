from bubblebuster.link import LinkMan, DLink

from enum import Enum

class BubbleNames(Enum):
    IRON = 1
    DELAY = 2
    NUKE = 3
    SLIPPERY = 4
    SPOTTED = 5
    TWIN = 6

class BubbleMan(LinkMan):
    instance = None
    def __init__(self):
        super().__init__()
        BubbleMan.instance = self

    def add(self, bubble):
        assert isinstance(bubble, type)
        self.base_add(DLink(bubble))
        return bubble

    def remove(self, bubble):
        self.base_remove(bubble)

    def compare(self, a, b):
        return a.name == b or a == b

    def find(self, bubble):
        return self.base_find(bubble)

    def update(self):
        head = self.head
        while head:
            head.update()
            head = head.next

    @staticmethod
    def set_active(manager):
        BubbleMan.instance = manager

