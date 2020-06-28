import pygame
from enum import Enum
from random import choice

from bubblebuster.settings import InterfaceSettings
from bubblebuster.link import *

class ImageNames(Enum):
    BOX = 2
    CIRCLE = 3
    EXPLODE = 4
    BLUEBUBBLE = 5
    CYANBUBBLE = 6
    GREENBUBBLE = 7
    ORANGEBUBBLE = 8
    PINKBUBBLE = 9
    REDBUBBLE = 10


class Image(Link):
    def __init__(self, name, data):
        super().__init__()
        self.name = name
        self.data = data
        if isinstance(data, str):
            self.surface = pygame.image.load(data).convert_alpha()
        elif len(data):
            self.surface = pygame.Surface(data[1])
            self.surface.fill(data[0])


class ImageMan(LinkMan):
    instance = None
    def __init__(self):
        super().__init__()
        ImageMan.instance = self

    def compare(self, a, b):
        return a.name == b

    def add(self, name, data):
        image = Image(name, data)
        self.base_add(image)

    def find(self, image):
        return self.base_find(image)

    @staticmethod
    def set_active(manager):
        ImageMan.instance = manager

