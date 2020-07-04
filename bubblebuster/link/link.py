import pygame
from random import randint

class SpriteLink(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.next = None
        self.prev = None
        self.collision_enabled = True

    def wash(self):
        self.next = None
        self.prev = None

    def print(self):
        raise NotImplementedError('this method is abstract')


class Link:
    instance = None
    def __init__(self):
        self.next = None
        self.prev = None

    def wash(self):
        self.next = None
        self.prev = None

    def print(self):
        raise NotImplementedError('this method is abstract')


class SpriteLinkMan(pygame.sprite.Group):
    def __init__(self, *sprites):
        pygame.sprite.Group.__init__(self, *sprites)


class Manager:
    def __init__(self):
        self.head = None
        self.length = 0

    def base_add(self, link):
        if not self.head:
            self.head = link
            return
        link.prev = None
        link.next = self.head
        self.head.prev = link
        self.head = link
        self.length += 1

    def base_remove_single(self, head):
        if head.next and not head.prev:
            head = head.next
            head.prev = None
            self.head = head
        elif head.next and head.prev:
            head.next.prev = head.prev
            head.prev.next = head.next
        else:
            if not head.prev: # only one on list
                self.head = None
            else:
                head.prev.next = None
        self.length -= 1

    def base_remove(self, link):
        head = self.head
        while head:
            if head == link:
                self.base_remove_single(head)
                return
            head = head.next

    def base_find(self, link):
        head = self.head
        while head:
            if self.compare(head, link):
                return head
            head = head.next


class LinkMan(Manager):
    instance = None

    def __init__(self):
        self.head = None
        super().__init__()

    def create(self):
        raise NotImplementedError('this is an abstract method')

    def compare(self, a, b):
        raise NotImplementedError('this is an abstract method')

    def wash(self):
        raise NotImplementedError('this is an abstract method')

    def print(self):
        head = self.head
        while head:
            head.print()
            head = head.next

    def get_random(self):
        head = self.head
        while head:
            if 1 / self.length >= randint(0, 100)/100:
                return head
            head = head.next
        return self.get_random()

    @staticmethod
    def set_active(manager):
        instance = manager
