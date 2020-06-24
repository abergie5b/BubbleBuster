import pygame
from enum import Enum

from link import *

class ImageNames(Enum):
    MOUSE = 1
    BOX = 2
    CIRCLE = 3
    EXPLODE = 4


class Image(Link):
    def __init__(self, name, data):
        super().__init__()
        self.name = name
        self.data = data
        if isinstance(data, str):
            self.surface = pygame.image.load(data)
        elif len(data):
            self.surface = pygame.Surface(data[1])
            self.surface.fill(data[0])


class ImageMan(LinkMan):
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

