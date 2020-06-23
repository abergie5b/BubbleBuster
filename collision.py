import pygame

from subject import *
from link import *

class CollisionPair(Subject):
    def __init__(self, objA, objB):
        super().__init__()
        self.objA = objA
        self.objB = objB
        self.enabled = True

    def collide(self):
        raise NotImplementedError("this is an abstract method")

    def process(self):
        self.collide()


class CollisionRectPair(CollisionPair):
    def collide(self):
        if self.enabled and pygame.sprite.collide_rect(self.objA, self.objB):
            self.objA.accept(self.objB)


class CollisionCirclePair(CollisionPair):
    def collide(self):
        if self.enabled and pygame.sprite.collide_circle(self.objA, self.objB):
            self.objA.accept(self.objB)


class CollisionPairMan(LinkMan):
    instance = None

    @staticmethod
    def create():
        if not CollisionPairMan.instance:
            CollisionPairMan.instance = CollisionPairMan.__new__(CollisionPairMan)
            CollisionPairMan.instance.head = None
        return CollisionPairMan.instance

    def compare(self, a, b):
        return a.name == b

    def add(self, collision_pair):
        # hotfix
        if collision_pair.objA != None and collision_pair.objB != None:
            self.base_add(collision_pair)

    def remove(self, sprite):
        head = self.head
        while head:
            if sprite == head.objA or sprite == head.objB:
                self.base_remove_single(head)
            head = head.next

    def process(self):
        head = self.head
        while head:
            head.process()
            head = head.next