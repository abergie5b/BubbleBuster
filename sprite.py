from image import ImageMan
from link import *

import enum

class SpriteNames(enum.Enum):
    MOUSE = 1


class Sprite(Link):
    def __init__(self, name, image_name, width, height, x, y):
        super().__init__()
        self.name = name
        self.image = ImageMan.find(image_name)

        # dimensions
        self.width = width
        self.height = height

        # position
        self.posx = x
        self.posy = y

        # for collisions
        self.colx = x
        self.coly = y

    def draw(self, screen):
        screen.blit(self.image.surface, (self.posx, self.posy))


class SpriteMan(LinkMan):
    @staticmethod
    def create():
        if not SpriteMan.instance:
            SpriteMan.instance = SpriteMan.__new__(SpriteMan)
            SpriteMan.instance.head = None

    @staticmethod
    def _get_instance():
        if not SpriteMan.instance:
            SpriteMan.instance = SpriteMan.create()
        return SpriteMan.instance

    @staticmethod
    def add(sprite_name, image_name, width, height, x, y):
        instance = SpriteMan._get_instance()
        head = instance.head
        link = Sprite(sprite_name, image_name, width, height, x, y)
        if not instance.head:
            instance.head = link
            return
        link.prev = None
        link.next = instance.head
        instance.head.prev = link
        instance.head = link

    @staticmethod
    def remove(link):
        instance = SpriteMan._get_instance()
        head = instance.head
        while head:
            if head == link:
                if head.next and not head.prev:
                    head = head.next
                    head.prev = None
                    instance.head = head
                elif head.next and head.prev:
                    head.next.prev = head.prev
                    head.prev.next = head.next
                else:
                    if not head.prev: # only one on list
                        instance.head = None
                    else:
                        head.prev.next = None
                return
            head = head.next

    @staticmethod
    def find(link):
        head = SpriteMan._get_instance().head
        while head:
            if head.name == link:
                return head
            head = head.next

    @staticmethod
    def print():
        head = SpriteMan._get_instance().head
        while head:
            head.print()
            head = head.next

    @staticmethod
    def draw(screen):
        head = SpriteMan._get_instance().head
        while head:
            head.draw(screen)
            head = head.next

