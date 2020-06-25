import pygame
from enum import Enum

from link import *

class SoundNames(Enum):
    MUSICMENU = 1
    BUBBLEPOP = 2
    SMALLEXPLODE = 3
    LARGEEXPLODE = 4


class Sound(Link):
    def __init__(self, name, filename):
        super().__init__()
        self.name = name
        self.filename = filename
        self.sound = pygame.mixer.Sound(filename)

    def play(self):
        self.sound.play()


class Music(Link):
    def __init__(self, name, filename):
        super().__init__()
        self.name = name
        self.filename = filename

    def play(self, loops=-1):
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()


class SoundMan(LinkMan):
    def compare(self, a, b):
        return a.name == b

    def add(self, name, data):
        image = Sound(name, data)
        self.base_add(image)

    def find(self, image):
        return self.base_find(image)

    @staticmethod
    def set_active(manager):
        SoundMan.instance = manager


