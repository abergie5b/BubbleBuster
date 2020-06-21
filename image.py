import pygame
from enum import Enum

from link import *

class ImageNames(Enum):
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
        return ImageMan.instance

    def compare(self, a, b):
        return a.name == b

    def add(self, name, path):
        image = Image(name, path)
        self.base_add(image)

