import pygame
import enum

from link import *

class ImageNames(enum.Enum):
    MOUSE = 1


class Image(Link):
    def __init__(self, name, path):
        super().__init__()
        self.name = name
        self.path = path
        self.surface = pygame.image.load(path)


class ImageMan(LinkMan):
    instance = None

    @staticmethod
    def create():
        if not ImageMan.instance:
            ImageMan.instance = ImageMan.__new__(ImageMan)
            ImageMan.instance.head = None

    @staticmethod
    def _get_instance():
        if not ImageMan.instance:
            ImageMan.instance = ImageMan.create()
        return ImageMan.instance

    @staticmethod
    def add(name, path):
        instance = ImageMan._get_instance()
        head = instance.head
        link = Image(name, path)
        if not instance.head:
            instance.head = link
            return
        link.prev = None
        link.next = instance.head
        instance.head.prev = link
        instance.head = link

    @staticmethod
    def remove(link):
        instance = ImageMan._get_instance()
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
        head = ImageMan._get_instance().head
        while head:
            if head.name == link:
                return head
            head = head.next

    @staticmethod
    def print():
        head = ImageMan._get_instance().head
        while head:
            head.print()
            head = head.next

    @staticmethod
    def draw(screen):
        head = ImageMan._get_instance().head
        while head:
            head.draw(screen)
            head = head.next

