import pygame

import bubblebuster.input.subject as subject
import bubblebuster.sprite as sp
from bubblebuster.link import *

def intersect(rectA, rectB):
    status = False
    if (rectA.width == 0 and rectA.height == 0):
        return status
    if (rectB.width == 0 and rectB.height == 0):
        return status
    
    aminx = rectA.x - rectA.width / 2
    amaxx = rectA.x + rectA.width / 2
    aminy = rectA.y - rectA.height / 2
    amaxy = rectA.y + rectA.height / 2

    bminx = rectB.x - rectB.width / 2
    bmaxx = rectB.x + rectB.width / 2
    bminy = rectB.y - rectB.height / 2
    bmaxy = rectB.y + rectB.height / 2

    if bmaxx < aminx or bminx > amaxx or bmaxy < aminy or bminy > amaxy:
        status = False
    else:
        status = True
    return status


class CollisionPair(subject.Subject):
    def __init__(self, objA, objB):
        super().__init__()
        self.objA = objA
        self.objB = objB

    def collide(self):
        raise NotImplementedError("this is an abstract method")

    def process(self):
        self.collide()


class CollisionRectPair(CollisionPair):
    def collide(self):
        if self.objA.collision_enabled and self.objB.collision_enabled:
            if pygame.sprite.collide_rect(self.objA, self.objB):
                self.objA.accept(self.objB)


class CollisionCirclePair(CollisionPair):
    def collide(self):
        if self.objA.collision_enabled and self.objB.collision_enabled:
            if pygame.sprite.collide_circle(self.objA, self.objB):
                self.objA.accept(self.objB)


class CollisionPairMan(LinkMan):
    instance = None

    def __init__(self):
        super().__init__()
        CollisionPairMan.instance = self

    def compare(self, a, b):
        return a.name == b

    def add(self, collision_pair):
        # hotfix
        if collision_pair.objA != None and collision_pair.objB != None:
            self.base_add(collision_pair)

    def add_groups(self, groupA, groupB, pair_function):
        '''
        attach collision pairs for each member of each group
        '''
        for a in groupA:
            for b in groupB:
                self.add(pair_function(a, b))

    def attach_to_group(self, group, sprite, pair_function, except_type=None):
        '''
        attach collision pairs for each (group[x], sprite) 
        '''
        for obj in group:
            # sprite cant collide with itself or exception type
            if obj != sprite and obj.type != except_type:
                self.add(pair_function(obj, sprite))

    def attach_to_group_asobja(self, group, sprite, pair_function, except_type=None):
        '''
        attach collision pairs for each (sprite, group[x]) 
        '''
        for obj in group:
            # sprite cant collide with itself or exception type
            if obj != sprite and obj.type != except_type:
                self.add(pair_function(sprite, obj))

    def remove_single(self, pair):
        head = self.head
        while head:
            if head == pair:
                self.base_remove_single(pair)
            head = head.next

    def remove_all_type(self, type):
        head = self.head
        while head:
            pair = head
            if type == head.objA.type or type == head.objB.type:
                self.base_remove_single(pair)
            head = head.next

    def remove(self, sprite):
        head = self.head
        while head:
            pair = head
            if sprite == head.objA or sprite == head.objB:
                self.base_remove_single(pair)
            head = head.next

    def process(self):
        head = self.head
        while head:
            head.process()
            head = head.next

    @staticmethod
    def set_active(manager):
        CollisionPairMan.instance = manager
