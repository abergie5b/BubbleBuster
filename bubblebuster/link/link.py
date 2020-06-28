import pygame

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
        raise NotImplementedError('this is an abstract class')

    def base_add(self, link):
        if not self.head:
            self.head = link
            return
        link.prev = None
        link.next = self.head
        self.head.prev = link
        self.head = link

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

    def create(self):
        raise NotImplementedError('this is an abstract method')

    def compare(self, a, b):
        raise NotImplementedError('this is an abstract method')

    def wash(self):
        raise NotImplementedError('this is an abstract method')

    def _get_instance(self):
        return instance

    def print(self):
        head = self.head
        while head:
            head.print()
            head = head.next

    @staticmethod
    def set_active(manager):
        instance = manager
