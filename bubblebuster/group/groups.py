from bubblebuster.link import LinkMan
import bubblebuster.collision as collision
import bubblebuster.sprite as sp
import bubblebuster.sprite as sp

from enum import Enum

class GroupNames(Enum):
    CIRCLE = 1
    WALL = 2


class Group(LinkMan):
    def __init__(self, name):
        self.head = None
        self.name = name
        self.nodeman = sp.SpriteNodeMan()

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
            # hotfix to disable circles colliding with themselves
            sprite = head.pSprite
            if circle.name == sp.BoxSpriteNames.EXPLOSION and sprite.name == sp.BoxSpriteNames.CIRCLE:
                collision.CollisionPairMan.instance.add(collision.CollisionCirclePair(circle, sprite))
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
