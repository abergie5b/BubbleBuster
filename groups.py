from link import LinkMan
from collision import CollisionPairMan, CollisionCirclePair
import sprite as sp
from spritenode import SpriteNodeMan

from enum import Enum

class GroupNames(Enum):
    CIRCLE = 1
    WALL = 2


class Group(LinkMan):
    def __init__(self, name):
        self.head = None
        self.name = name
        self.nodeman = SpriteNodeMan()

    def add(self, spritenode):
        self.nodeman.add(spritenode)

    def remove(self, spritenode):
        self.nodeman.remove(spritenode)

    def __iter__(self):
        head = self.nodeman.head
        while head:
            yield head.pSprite
            head = head.next


class CircleGroup(Group):
    def __init__(self, name):
        super().__init__(name)

    def add(self, circle):
        # circles can collide with explosions
        # so add the new circle to the collision man
        head = self.nodeman.head
        while head:
            # hotfix
            sprite = head.pSprite
            if circle.name == sp.BoxSpriteNames.EXPLOSION and sprite.name == sp.BoxSpriteNames.CIRCLE:
                CollisionPairMan.instance.add(CollisionCirclePair(circle, sprite))
            head = head.next
        self.nodeman.add(circle)

    def remove(self, circle):
        self.nodeman.remove(circle)

    def find(self, circle):
        return self.nodeman.base_find(circle)


class GroupMan(LinkMan):
    instance = None

    def add(self, group):
        self.base_add(group)

    def compare(self, a, b):
        return a.name == b or a == b

    def find(self, group):
        return self.base_find(group)
 
    @staticmethod
    def set_active(manager):
        GroupMan.instance = manager
